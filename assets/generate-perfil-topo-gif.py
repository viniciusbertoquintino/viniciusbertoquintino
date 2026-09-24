"""Gera assets/perfil-topo.gif a partir de assets/perfil-topo.png."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "perfil-topo.png"
DST = ROOT / "perfil-topo.gif"

# Animação + pausa antes do loop (~0,85 s com FRAME_MS=85)
N_MOVE = 22
N_PAUSE = 9
FRAME_MS = 85
MAX_WIDTH = 960
PALETTE_COLORS = 96


def trace_path(lum: np.ndarray, x_start: int, x_end: int, y_seed: float) -> tuple[np.ndarray, np.ndarray]:
    h = lum.shape[0]
    xs = np.arange(x_start, x_end, dtype=np.int32)
    ys: list[int] = []
    prev = int(y_seed)
    for x in xs:
        y0 = max(0, prev - 32)
        y1 = min(h, prev + 32)
        band = lum[y0:y1, x]
        prev = int(y0 + int(band.argmax()))
        ys.append(prev)
    ys_arr = np.asarray(ys, dtype=np.float32)
    kernel = np.ones(25) / 25
    ys_arr = np.convolve(np.pad(ys_arr, 12, mode="edge"), kernel, mode="valid")
    return xs, ys_arr


def find_amber_nodes(base: np.ndarray, lum: np.ndarray) -> list[tuple[float, float]]:
    r, g, b = base[:, :, 0], base[:, :, 1], base[:, :, 2]
    mask = (r > 90) & (g > 70) & (r > b + 25) & (lum > 55)
    if not mask.any():
        return [(820.0, 260.0), (920.0, 265.0)]
    ys, xs = np.nonzero(mask)
    order = np.argsort(xs)
    xs, ys = xs[order], ys[order]
    clusters: list[list[tuple[int, int]]] = []
    for x, y in zip(xs, ys):
        if not clusters or x - clusters[-1][-1][0] > 35:
            clusters.append([(int(x), int(y))])
        else:
            clusters[-1].append((int(x), int(y)))
    nodes: list[tuple[float, float]] = []
    for cluster in clusters:
        if len(cluster) < 8:
            continue
        cx = float(np.mean([p[0] for p in cluster]))
        cy = float(np.mean([p[1] for p in cluster]))
        nodes.append((cx, cy))
    return nodes[:2] if len(nodes) >= 2 else [(820.0, 260.0), (920.0, 265.0)]


def add_glow(
    img: np.ndarray,
    cx: float,
    cy: float,
    radius: float,
    strength: float,
    color: np.ndarray,
) -> None:
    h, w = img.shape[:2]
    span = int(radius * 3.5)
    y0b = max(0, int(cy - span))
    y1b = min(h, int(cy + span))
    x0b = max(0, int(cx - span))
    x1b = min(w, int(cx + span))
    yy, xx = np.mgrid[y0b:y1b, x0b:x1b]
    d2 = (yy - cy) ** 2 + (xx - cx) ** 2
    sigma = radius * 0.75
    g = np.exp(-d2 / (2 * sigma * sigma)) * strength
    img[y0b:y1b, x0b:x1b] += g[..., None] * color


def render_frame(
    base: np.ndarray,
    xs: np.ndarray,
    ys: np.ndarray,
    head: int,
    amber_nodes: list[tuple[float, float]],
    tail_len: int,
) -> np.ndarray:
    del tail_len  # cometa de comprimento fixo
    img = base.copy()
    w = base.shape[1]
    head_x = float(xs[head])
    second_amber_x = amber_nodes[1][0] if len(amber_nodes) > 1 else head_x + 999
    final_boost = 1.0 + 0.4 * min(1.0, max(0.0, (head_x - second_amber_x) / (w * 0.1)))

    for back, strength, radius in ((0, 0.46, 13), (14, 0.24, 10), (30, 0.11, 8), (50, 0.05, 7)):
        k = head - back
        if k < 0:
            continue
        px = float(xs[k])
        py = float(ys[k])
        amber_zone = min(1.0, max(0.0, (px - w * 0.61) / (w * 0.16)))
        color = np.array(
            [45 + 175 * amber_zone, 155 - 25 * amber_zone, 255 - 155 * amber_zone],
            dtype=np.float32,
        )
        boost = final_boost if px >= second_amber_x - 15 else 1.0
        add_glow(img, px, py, radius, strength * boost, color)

    for ax, ay in amber_nodes:
        if head_x >= ax - 14:
            warm = np.array([255, 185, 85], dtype=np.float32)
            pulse = min(1.0, max(0.0, (head_x - ax + 14) / 42))
            add_glow(img, ax, ay, 18, 0.16 * pulse, warm)

    np.clip(img, 0, 255, out=img)
    return img


def main() -> None:
    src = Image.open(SRC).convert("RGB")
    if src.width > MAX_WIDTH:
        scale = MAX_WIDTH / src.width
        src = src.resize(
            (MAX_WIDTH, max(1, int(src.height * scale))),
            Image.Resampling.LANCZOS,
        )
    base = np.asarray(src).astype(np.float32)
    h, w, _ = base.shape
    lum = 0.15 * base[:, :, 0] + 0.45 * base[:, :, 1] + base[:, :, 2]

    xs, ys = trace_path(lum, int(w * 0.10), int(w * 0.81), h * 0.52)
    amber_nodes = find_amber_nodes(base, lum)

    move_frames: list[Image.Image] = []
    for i in range(N_MOVE):
        t = i / (N_MOVE - 1)
        head = int(t * (len(xs) - 1))
        arr = render_frame(base, xs, ys, head, amber_nodes, 0)
        move_frames.append(Image.fromarray(arr.astype(np.uint8)))

    pause_frame = move_frames[-1]
    frames = move_frames + [pause_frame.copy() for _ in range(N_PAUSE)]

    sheet = Image.new("RGB", (w, h * 4))
    for j, idx in enumerate((0, N_MOVE // 2, N_MOVE - 1, len(frames) - 1)):
        sheet.paste(frames[idx], (0, j * h))
    palette = sheet.quantize(colors=PALETTE_COLORS, method=Image.Quantize.MEDIANCUT)
    quantized = [frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in frames]

    quantized[0].save(
        DST,
        save_all=True,
        append_images=quantized[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
        disposal=2,
    )
    size_mb = DST.stat().st_size / (1024 * 1024)
    print(f"{DST}  {size_mb:.2f} MB  {w}x{h}  {len(frames)} frames")


if __name__ == "__main__":
    main()

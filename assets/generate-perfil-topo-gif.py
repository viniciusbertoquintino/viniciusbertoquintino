"""Desenha o banner do perfil: uma execução dentro do motor do agente.

Sem texto na imagem. O PNG é o quadro final; o GIF é a mesma cena animada.
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
PNG = ROOT / "perfil-topo.png"
GIF = ROOT / "perfil-topo.gif"

W, H = 1400, 460
GIF_W = 1000
SCALE = 2

N_REST = 4
N_MOVE = 42
FRAME_MS = 100
PAUSE_MS = 800
PALETTE_COLORS = 128

BG = (7, 11, 20)
ENGINE_FILL = (11, 17, 31)
ENGINE_STROKE = (42, 96, 138)
EDGE_DIM = (32, 64, 96)
EDGE_LIT = (86, 168, 232)
NODE_DIM = (38, 78, 118)
NODE_LIT = (186, 224, 255)
AMBER = (232, 168, 78)
DOT_DIM = (28, 58, 88)
DOT_LIT = (150, 206, 255)
PACKET = np.array([210, 236, 255], dtype=np.float32)
PACKET_AMBER = np.array([255, 196, 120], dtype=np.float32)

ENGINE = (210, 52, 920, 408)
NODE_R = 11
INSET = 20

INPUT = (78, 230)
CONTEXT = (340, 230)
REASONING = (560, 124)
TOOL = (780, 230)
OBSERVATION = (560, 324)
WALL = (920, 324)
RESULT = (1188, 230)

# Quatro indicadores na base: acendem com contexto, raciocínio, ferramenta e observação.
DOTS = ((455, 382), (525, 382), (595, 382), (665, 382))

PATH = [INPUT, CONTEXT, REASONING, TOOL, OBSERVATION, WALL, RESULT]
RETURN = (OBSERVATION, CONTEXT)
# gap na saída e na chegada; o ponto da borda não é nó, então a linha atravessa o motor.
EDGES = (
    (INPUT, CONTEXT, INSET, INSET, True),
    (CONTEXT, REASONING, INSET, INSET, True),
    (REASONING, TOOL, INSET, INSET, True),
    (TOOL, OBSERVATION, INSET, INSET, True),
    (OBSERVATION, WALL, INSET, 0, False),
    (WALL, RESULT, 0, INSET, True),
)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = min(1.0, max(0.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def lerp(a: tuple[float, float], b: tuple[float, float], t: float) -> tuple[float, float]:
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(b[0] - a[0], b[1] - a[1])


def inset_segment(
    a: tuple[float, float],
    b: tuple[float, float],
    gap_a: float,
    gap_b: float,
) -> tuple[tuple[float, float], tuple[float, float]]:
    length = dist(a, b)
    if length < 1:
        return a, b
    if gap_a + gap_b >= length:
        gap_a = length * 0.2
        gap_b = length * 0.2
    ux, uy = (b[0] - a[0]) / length, (b[1] - a[1]) / length
    start = (a[0] + ux * gap_a, a[1] + uy * gap_a)
    end = (b[0] - ux * gap_b, b[1] - uy * gap_b)
    return start, end


def build_samples(step: float = 7.0) -> list[tuple[float, float, int, float]]:
    samples: list[tuple[float, float, int, float]] = []
    for seg, (a, b) in enumerate(zip(PATH, PATH[1:])):
        length = dist(a, b)
        n = max(2, int(round(length / step)))
        for s in range(n):
            if seg > 0 and s == 0:
                continue
            local = s / (n - 1)
            samples.append((*lerp(a, b, local), seg, local))
    return samples


def sc(point: tuple[float, float]) -> tuple[float, float]:
    return (point[0] * SCALE, point[1] * SCALE)


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill: tuple[int, int, int],
) -> None:
    ang = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 13 * SCALE
    tip = sc(end)
    left = (
        tip[0] - size * math.cos(ang - 0.42),
        tip[1] - size * math.sin(ang - 0.42),
    )
    right = (
        tip[0] - size * math.cos(ang + 0.42),
        tip[1] - size * math.sin(ang + 0.42),
    )
    draw.polygon([tip, left, right], fill=fill)


def draw_edge(
    draw: ImageDraw.ImageDraw,
    a: tuple[float, float],
    b: tuple[float, float],
    fill: tuple[int, int, int],
    progress: float,
    width: int,
    gap_a: float = INSET,
    gap_b: float = INSET,
    arrow: bool = True,
) -> None:
    if progress <= 0.02:
        return
    start, end = inset_segment(a, b, gap_a, gap_b)
    tip = lerp(start, end, min(1.0, progress))
    draw.line([sc(start), sc(tip)], fill=fill, width=width)
    if arrow and progress >= 0.96:
        draw_arrow(draw, start, end, fill)


def add_glow(
    img: np.ndarray,
    cx: float,
    cy: float,
    radius: float,
    strength: float,
    color: np.ndarray,
) -> None:
    if strength <= 0.01:
        return
    h, w = img.shape[:2]
    span = int(radius * 3.2)
    x0, x1 = max(0, int(cx - span)), min(w, int(cx + span) + 1)
    y0, y1 = max(0, int(cy - span)), min(h, int(cy + span) + 1)
    if x0 >= x1 or y0 >= y1:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    sigma = max(1.0, radius * 0.7)
    glow = np.exp(-((yy - cy) ** 2 + (xx - cx) ** 2) / (2 * sigma * sigma)) * strength
    img[y0:y1, x0:x1] += glow[..., None] * color


def _amber(seg: int, local: float) -> float:
    if seg == 2:
        return min(1.0, max(0.0, (local - 0.28) / 0.32))
    if seg == 3:
        return min(1.0, max(0.0, 1.0 - max(0.0, local - 0.05) / 0.5))
    return 0.0


def arrival(seg: int, local: float, gate: int) -> float:
    if seg > gate:
        return 1.0
    if seg < gate:
        return 0.0
    return min(1.0, max(0.0, (local - 0.68) / 0.32))


def edge_progress(seg: int, local: float, edge: int) -> float:
    if seg > edge:
        return 1.0
    if seg == edge:
        return local
    return 0.0


def points_behind(
    samples: list[tuple[float, float, int, float]],
    index: int,
    distances: tuple[int, ...],
) -> list[tuple[float, float]]:
    if index <= 0:
        return []
    prev = (samples[index][0], samples[index][1])
    walked = 0.0
    found: list[tuple[float, float]] = []
    target = 0
    for j in range(index - 1, -1, -1):
        point = (samples[j][0], samples[j][1])
        walked += dist(prev, point)
        prev = point
        if walked >= distances[target]:
            found.append(point)
            target += 1
            if target >= len(distances):
                break
    return found


def render(sample: tuple[float, float, int, float] | None, samples_behind: list[tuple[float, float]]) -> Image.Image:
    hi = Image.new("RGB", (W * SCALE, H * SCALE), BG)
    draw = ImageDraw.Draw(hi)
    box = [v * SCALE for v in ENGINE]
    draw.rounded_rectangle(box, radius=28 * SCALE, fill=ENGINE_FILL, outline=ENGINE_STROKE, width=4)

    if sample is None:
        seg, local = -1, 0.0
        packet = None
        amber = 0.0
    else:
        seg, local = sample[2], sample[3]
        packet = (sample[0], sample[1])
        amber = _amber(seg, local)

    for index, (a, b, gap_a, gap_b, arrow) in enumerate(EDGES):
        draw_edge(draw, a, b, EDGE_DIM, 1.0, 4, gap_a, gap_b, arrow)
        lit = edge_progress(seg, local, index)
        draw_edge(draw, a, b, EDGE_LIT, lit, 4, gap_a, gap_b, arrow)

    ret = 1.0 if arrival(seg, local, 3) > 0.85 else 0.0
    draw_edge(draw, RETURN[0], RETURN[1], EDGE_DIM, 1.0, 4)
    draw_edge(draw, RETURN[0], RETURN[1], EDGE_LIT, ret, 4)

    amounts = {
        "context": arrival(seg, local, 0),
        "reasoning": arrival(seg, local, 1),
        "tool": arrival(seg, local, 2),
        "observation": arrival(seg, local, 3),
        "result": arrival(seg, local, 5),
    }
    nodes = {
        "input": INPUT,
        "context": CONTEXT,
        "reasoning": REASONING,
        "tool": TOOL,
        "observation": OBSERVATION,
        "result": RESULT,
    }
    for name, point in nodes.items():
        amount = amounts.get(name, 0.0)
        if name == "tool" and amber > 0:
            color = mix(mix(NODE_DIM, NODE_LIT, amount), AMBER, amber)
        elif name == "input":
            color = mix(NODE_DIM, NODE_LIT, amounts["context"])
        else:
            color = mix(NODE_DIM, NODE_LIT, amount)
        c = sc(point)
        r = NODE_R * SCALE
        draw.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=color)

    dot_gates = (0, 1, 2, 3)
    for dot, gate in zip(DOTS, dot_gates):
        amount = arrival(seg, local, gate)
        color = mix(DOT_DIM, DOT_LIT, amount)
        c = sc(dot)
        r = (3.2 + amount) * SCALE
        draw.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), fill=color)

    frame = hi.resize((W, H), Image.Resampling.LANCZOS)
    img = np.asarray(frame).astype(np.float32)

    for name, point in nodes.items():
        amount = amounts.get(name, 0.0)
        if name == "input":
            amount = amounts["context"] * 0.85
        if name == "tool" and amber > 0:
            add_glow(img, point[0], point[1], 22, 0.16 * amber, np.array(AMBER, dtype=np.float32))
            amount *= 1 - amber
        if amount > 0.05:
            strength = 0.2 * amount
            if name == "result":
                strength = 0.28 * amount
            add_glow(img, point[0], point[1], 18, strength, np.array(NODE_LIT, dtype=np.float32))

    for dot, gate in zip(DOTS, dot_gates):
        amount = arrival(seg, local, gate)
        if amount > 0.2:
            add_glow(img, dot[0], dot[1], 8, 0.18 * amount, np.array(DOT_LIT, dtype=np.float32))

    if packet is not None:
        tone = PACKET * (1 - amber) + PACKET_AMBER * amber
        for index, point in enumerate(samples_behind):
            fade = (0.3, 0.16, 0.07)[index] if index < 3 else 0.05
            add_glow(img, point[0], point[1], 8, fade, tone)
        add_glow(img, packet[0], packet[1], 15, 0.42, tone)
        add_glow(img, packet[0], packet[1], 4.5, 0.85, np.array([245, 250, 255], dtype=np.float32))

    np.clip(img, 0, 255, out=img)
    return Image.fromarray(img.astype(np.uint8))


def main() -> None:
    samples = build_samples()
    frames: list[Image.Image] = []
    for i in range(N_REST):
        frames.append(render(None, []))
    last = len(samples) - 1
    for i in range(N_MOVE):
        t = i / (N_MOVE - 1)
        index = min(last, int(round(t * last)))
        behind = points_behind(samples, index, (18, 40, 66))
        frames.append(render(samples[index], behind))

    frames[-1].save(PNG, optimize=True)

    gif_h = round(H * GIF_W / W)
    gif_frames = [
        frame.resize((GIF_W, gif_h), Image.Resampling.LANCZOS) for frame in frames
    ]
    sheet = Image.new("RGB", (GIF_W, gif_h * 4))
    peak = max(range(len(samples)), key=lambda i: _amber(samples[i][2], samples[i][3]))
    amber_frame = N_REST + int(round(peak / (len(samples) - 1) * (N_MOVE - 1)))
    picks = (0, max(0, amber_frame - 8), amber_frame, len(gif_frames) - 1)
    for row, index in enumerate(picks):
        sheet.paste(gif_frames[index], (0, row * gif_h))
    palette = sheet.quantize(colors=PALETTE_COLORS, method=Image.Quantize.FASTOCTREE)
    quantized = [
        frame.quantize(palette=palette, dither=Image.Dither.NONE) for frame in gif_frames
    ]
    durations = [FRAME_MS] * (len(quantized) - 1) + [PAUSE_MS]
    quantized[0].save(
        GIF,
        save_all=True,
        append_images=quantized[1:],
        duration=durations,
        loop=0,
        optimize=True,
        disposal=2,
    )
    size_mb = GIF.stat().st_size / (1024 * 1024)
    print(f"{GIF.name}  {size_mb:.2f} MB  {GIF_W}x{gif_h}  {len(quantized)} frames")
    print(f"{PNG.name}  {PNG.stat().st_size / 1024:.0f} KB  {W}x{H}")


if __name__ == "__main__":
    main()

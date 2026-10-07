"""Converte assets/source-prepped.png num SVG que se digita uma vez.

Uso: python scripts/make_ascii_svg.py
STATIC=1 grava o quadro final, sem animação, para preview local.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = ROOT / "assets" / "source-prepped.png"
DEFAULT_OUT = ROOT / "ascii.svg"

RAMP = " .`:-=+*cs#%@"
COLS = 100
ROWS = 53
FONT = 13
CHAR_W = 8
ROW_H = 15
PAD = 18
# Largura do glifo / altura da linha. Compensa o caractere mais alto que largo.
CHAR_ASPECT = CHAR_W / ROW_H
NAVY = "#070B14"
STROKE = "#2A608A"
INK = "#C9D1D9"
CURSOR = "#56A8E8"
WIPE_S = 0.45
STAGGER_S = 0.07


def xml_escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def trim_subject(image):
    """Corta a margem branca e aproxima o quadro no rosto."""
    import numpy as np

    values = np.asarray(image)
    height, width = values.shape
    upper = values[: int(height * 0.78)]
    mask = upper < 200
    if not mask.any():
        return image
    rows_hit = np.where(mask.any(axis=1))[0]
    cols_hit = np.where(mask.any(axis=0))[0]
    top, bottom = int(rows_hit[0]), int(rows_hit[-1])
    left, right = int(cols_hit[0]), int(cols_hit[-1])
    head_h = max(1, bottom - top)
    bottom = min(height - 1, bottom + int(head_h * 0.55))
    pad_x = max(2, int((right - left) * 0.06))
    pad_y = max(2, int(head_h * 0.04))
    return image.crop(
        (
            max(0, left - pad_x),
            max(0, top - pad_y),
            min(width, right + pad_x + 1),
            min(height, bottom + 1),
        )
    )


def stretch_contrast(pixels: bytes) -> bytes:
    """Empurra o fundo para espaço e separa cabelo, óculos e pele."""
    import numpy as np

    values = np.frombuffer(pixels, dtype=np.uint8).astype(np.float32)
    subject = values[values < 242]
    if subject.size < 10:
        return pixels
    low = float(np.percentile(subject, 5))
    high = float(np.percentile(subject, 97))
    if high <= low:
        return pixels
    scaled = np.clip((values - low) / (high - low), 0.0, 1.0) ** 0.75
    out = (scaled * 255).astype(np.uint8)
    # O fundo de papel vira espaço. O lado claro do rosto continua com um glifo leve,
    # senão a silhueta some no painel escuro.
    paper = values >= 250
    out[paper] = 255
    out[~paper] = np.minimum(out[~paper], 200)
    return out.tobytes()


def cover(image, cols: int, rows: int):
    from PIL import Image

    target = (cols * CHAR_ASPECT) / rows
    width, height = image.size
    aspect = width / height if height else target
    if aspect > target:
        crop_w = max(1, int(round(height * target)))
        left = max(0, (width - crop_w) // 2)
        image = image.crop((left, 0, left + crop_w, height))
    else:
        crop_h = max(1, int(round(width / target)))
        top = max(0, (height - crop_h) // 2)
        image = image.crop((0, top, width, top + crop_h))
    return image.resize((cols, rows), Image.Resampling.LANCZOS)


def glyph(brightness: int) -> str:
    # 255 (branco, fundo) -> espaço. 0 (escuro) -> caractere denso.
    span = len(RAMP) - 1
    index = round((1.0 - brightness / 255.0) * span)
    return RAMP[max(0, min(span, index))]


def rows_from(path: Path) -> list[str]:
    from PIL import Image

    image = trim_subject(Image.open(path).convert("L"))
    small = cover(image, COLS, ROWS)
    pixels = stretch_contrast(small.tobytes())
    lines = []
    for row in range(ROWS):
        start = row * COLS
        lines.append("".join(glyph(v) for v in pixels[start : start + COLS]))
    return lines


def render(lines: list[str], static: bool) -> str:
    text_w = COLS * CHAR_W
    width = text_w + PAD * 2
    height = ROWS * ROW_H + PAD * 2
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'role="img" aria-label="Retrato ASCII">'
        ),
        "<title>Retrato ASCII</title>",
        (
            f'<rect width="{width}" height="{height}" rx="18" fill="{NAVY}" '
            f'stroke="{STROKE}" stroke-width="2"/>'
        ),
        "<defs>",
    ]
    for index in range(ROWS):
        y = PAD + index * ROW_H
        delay = f"{index * STAGGER_S:.2f}s"
        if static:
            wipe = f'<rect x="0" y="{y}" width="{width}" height="{ROW_H}"/>'
        else:
            wipe = (
                f'<rect x="0" y="{y}" width="0" height="{ROW_H}">'
                f'<animate attributeName="width" from="0" to="{width}" dur="{WIPE_S}s" '
                f'begin="{delay}" fill="freeze"/>'
                "</rect>"
            )
        parts.append(f'<clipPath id="row-{index}">{wipe}</clipPath>')
    parts.append("</defs>")

    baseline_shift = 11
    for index, line in enumerate(lines):
        y = PAD + index * ROW_H
        parts.append(
            f'<g clip-path="url(#row-{index})">'
            f'<text x="{PAD}" y="{y + baseline_shift}" fill="{INK}" '
            f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" '
            f'font-size="{FONT}" xml:space="preserve" '
            f'textLength="{text_w}" lengthAdjust="spacingAndGlyphs">'
            f"{xml_escape(line)}</text></g>"
        )

    if not static:
        for index in range(ROWS):
            y = PAD + index * ROW_H
            begin = index * STAGGER_S
            end = begin + WIPE_S
            parts.append(
                f'<rect x="{PAD}" y="{y + 1}" width="{CHAR_W - 1}" height="{ROW_H - 3}" '
                f'fill="{CURSOR}" opacity="0">'
                f'<set attributeName="opacity" to="1" begin="{begin:.2f}s" fill="freeze"/>'
                f'<animate attributeName="x" from="{PAD}" to="{PAD + text_w}" '
                f'dur="{WIPE_S}s" begin="{begin:.2f}s" fill="freeze"/>'
                f'<set attributeName="opacity" to="0" begin="{end:.2f}s" fill="freeze"/>'
                "</rect>"
            )

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera o SVG do retrato ASCII.")
    parser.add_argument("--src", default=str(DEFAULT_SRC))
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    src = Path(args.src)
    if not src.is_file():
        raise SystemExit(f"imagem preparada não encontrada: {src}")
    out = Path(args.out)
    out.write_text(render(rows_from(src), os.environ.get("STATIC") == "1"), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()

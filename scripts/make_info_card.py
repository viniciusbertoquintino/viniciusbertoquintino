"""Cartão no estilo neofetch. As linhas entram uma vez e param.

Uso: python scripts/make_info_card.py
STATIC=1 grava o quadro final, sem animação, para preview local.
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "info-card.svg"

NAVY = "#070B14"
STROKE = "#2A608A"
CYAN = "#56A8E8"
AMBER = "#E8A84E"
INK = "#E6EDF3"

WIDTH = 1040
HEIGHT = 460
# (chave, valor, cor do valor)
ROWS = (
    ("Now", "AI Engineer", INK),
    ("Focus", "LLMs · Agentes · RAG", INK),
    ("Stack", "Python · Rust · React · FastAPI", INK),
    ("Highlights", "Pix Race · Jev · Production RAG · plataforma", AMBER),
)


def line_motion(index: int, static: bool) -> str:
    if static:
        return ""
    begin = 0.08 + index * 0.14
    return (
        f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" '
        f'begin="{begin:.2f}s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0 8" to="0 0" dur="0.4s" begin="{begin:.2f}s" fill="freeze"/>'
    )


def render(static: bool) -> str:
    font = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
    blocks: list[str] = []
    blocks.append(
        f'<text x="48" y="78" font-family="{font}" font-size="34">'
        f'<tspan fill="{CYAN}">vinicius</tspan>'
        f'<tspan fill="{AMBER}">@github</tspan></text>'
    )
    blocks.append(
        f'<line x1="48" y1="108" x2="992" y2="108" stroke="{STROKE}" stroke-width="2"/>'
    )
    for key, value, color in ROWS:
        y = 178 + (len(blocks) - 2) * 64
        blocks.append(
            f'<text font-family="{font}" font-size="28" y="{y}">'
            f'<tspan x="48" fill="{CYAN}">{key}</tspan>'
            f'<tspan x="300" fill="{color}">{value}</tspan></text>'
        )

    body = "\n".join(
        f'  <g opacity="{"1" if static else "0"}">{markup}{line_motion(index, static)}</g>'
        for index, markup in enumerate(blocks)
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-label="Cartão do perfil">
  <title>vinicius@github</title>
  <rect width="{WIDTH}" height="{HEIGHT}" rx="18" fill="{NAVY}" stroke="{STROKE}" stroke-width="2"/>
{body}
</svg>
"""


def main() -> None:
    OUT.write_text(render(os.environ.get("STATIC") == "1"), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()

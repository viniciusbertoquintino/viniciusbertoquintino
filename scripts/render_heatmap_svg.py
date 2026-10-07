"""Desenha data/contributions.json como um calendário que entra na diagonal.

Uso: python scripts/render_heatmap_svg.py
STATIC=1 grava o quadro final, sem animação, para preview local.
"""

from __future__ import annotations

import json
import os
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

# Nível 0 até o verde mais claro que o GitHub usa no nível 4.
PALETTE = ("#161b22", "#0e4429", "#006d32", "#26a641", "#39d353")
MONTHS = ("", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
DOW = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
SHOW_DOW = {"Mon", "Wed", "Fri"}

NAVY = "#070B14"
STROKE = "#2A608A"
MUTED = "#8B949E"
INK = "#E6EDF3"

CELL = 11
GAP = 3
STEP = CELL + GAP
PAD = 20
LABEL_W = 32
LABEL_H = 18


def color(level: int) -> str:
    return PALETTE[max(0, min(level, len(PALETTE) - 1))]


def month_columns(days: list[dict]) -> dict[int, str]:
    by_col: dict[int, list[date]] = {}
    for item in days:
        by_col.setdefault(item["col"], []).append(date.fromisoformat(item["date"]))
    labels: dict[int, str] = {}
    seen: set[tuple[int, int]] = set()
    for col in sorted(by_col):
        for current in sorted(by_col[col]):
            key = (current.year, current.month)
            if current.day == 1 and key not in seen:
                labels[col] = MONTHS[current.month]
                seen.add(key)
    if by_col and 0 not in labels:
        first = min(by_col[0])
        labels[0] = MONTHS[first.month]
    # Dois meses muito próximos se sobrepõem no desenho.
    placed: dict[int, str] = {}
    last = -99
    for col in sorted(labels):
        if col - last < 3 and col != 0:
            continue
        placed[col] = labels[col]
        last = col
    return placed


def row_labels(days: list[dict]) -> dict[int, str]:
    seen: dict[int, date] = {}
    for item in days:
        row = item["row"]
        if row not in seen:
            seen[row] = date.fromisoformat(item["date"])
    labels = {}
    for row, current in seen.items():
        name = DOW[current.weekday()]
        if name in SHOW_DOW:
            labels[row] = name
    return labels


def render(payload: dict, static: bool) -> str:
    days = payload["days"]
    if not days:
        raise SystemExit("contributions.json não tem dias")
    cols = max(item["col"] for item in days) + 1
    rows = max(item["row"] for item in days) + 1
    origin_x = PAD + LABEL_W
    origin_y = PAD + LABEL_H
    grid_w = cols * STEP - GAP
    grid_h = rows * STEP - GAP
    width = origin_x + grid_w + PAD
    footer_y = origin_y + grid_h + 28
    height = footer_y + PAD

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'role="img" aria-label="{payload["total"]} contributions in the last year">'
        ),
        f"<title>{payload['total']} contributions in the last year</title>",
        (
            f'<rect width="{width}" height="{height}" rx="18" fill="{NAVY}" '
            f'stroke="{STROKE}" stroke-width="2"/>'
        ),
    ]

    font = "ui-sans-serif, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"
    for col, name in month_columns(days).items():
        x = origin_x + col * STEP
        parts.append(
            f'<text x="{x}" y="{PAD + 12}" fill="{MUTED}" font-family="{font}" '
            f'font-size="12">{name}</text>'
        )
    for row, name in row_labels(days).items():
        y = origin_y + row * STEP + CELL - 1
        parts.append(
            f'<text x="{PAD + LABEL_W - 8}" y="{y}" fill="{MUTED}" font-family="{font}" '
            f'font-size="11" text-anchor="end">{name}</text>'
        )

    for item in days:
        x = origin_x + item["col"] * STEP
        y = origin_y + item["row"] * STEP
        begin = (item["col"] + item["row"]) * 0.04
        motion = ""
        opacity = "1"
        if not static:
            opacity = "0"
            motion = (
                f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" '
                f'begin="{begin:.2f}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" '
                f'from="0 -7" to="0 0" dur="0.45s" begin="{begin:.2f}s" fill="freeze"/>'
            )
        parts.append(
            f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" '
            f'fill="{color(item["level"])}" opacity="{opacity}">'
            f"{motion}<title>{item['date']}: {item['count']}</title></rect>"
        )

    total = f"{payload['total']:,}"
    parts.append(
        f'<text x="{origin_x}" y="{footer_y}" fill="{INK}" font-family="{font}" '
        f'font-size="14">{total} contributions in the last year</text>'
    )

    legend_x = origin_x + grid_w - (len(PALETTE) * (CELL + 4) + 78)
    legend_y = footer_y - 11
    parts.append(
        f'<text x="{legend_x}" y="{legend_y + 10}" fill="{MUTED}" font-family="{font}" '
        f'font-size="12">Less</text>'
    )
    square = legend_x + 36
    for index, swatch in enumerate(PALETTE):
        parts.append(
            f'<rect x="{square + index * (CELL + 4)}" y="{legend_y}" width="{CELL}" '
            f'height="{CELL}" rx="2" fill="{swatch}"/>'
        )
    more_x = square + len(PALETTE) * (CELL + 4) + 4
    parts.append(
        f'<text x="{more_x}" y="{legend_y + 10}" fill="{MUTED}" font-family="{font}" '
        f'font-size="12">More</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    if not SRC.is_file():
        raise SystemExit(f"arquivo não encontrado: {SRC}")
    payload = json.loads(SRC.read_text(encoding="utf-8"))
    OUT.write_text(render(payload, os.environ.get("STATIC") == "1"), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()

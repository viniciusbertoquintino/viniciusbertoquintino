"""Baixa o calendário público de contribuições, sem token.

Fonte: https://github.com/users/<usuário>/contributions
Saída: data/contributions.json
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = "viniciusbertoquintino"
URL = f"https://github.com/users/{USERNAME}/contributions"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "contributions.json"

CELL_ID = re.compile(r"contribution-day-component-(\d+)-(\d+)")
COUNT = re.compile(r"(\d+)\s+contribution", re.IGNORECASE)
REPORTED = re.compile(r"([\d,]+)\s+contributions?\s+in the last year", re.IGNORECASE)


def parse_count(text: str, level: int) -> int:
    cleaned = " ".join(text.split())
    if cleaned.lower().startswith("no contribution"):
        return 0
    match = COUNT.search(cleaned)
    if match:
        return int(match.group(1))
    return 0 if level == 0 else level


def current_streak(days: list[dict]) -> int:
    if not days:
        return 0
    today = {
        date.today().isoformat(),
        datetime.now(timezone.utc).date().isoformat(),
    }
    end = days[:-1] if days[-1]["date"] in today and days[-1]["count"] == 0 else days
    streak = 0
    for item in reversed(end):
        if item["count"] <= 0:
            break
        streak += 1
    return streak


def longest_streak(days: list[dict]) -> int:
    best = run = 0
    for item in days:
        if item["count"] > 0:
            run += 1
            best = max(best, run)
        else:
            run = 0
    return best


def fetch_html() -> str:
    response = requests.get(
        URL,
        headers={
            "User-Agent": "viniciusbertoquintino-profile-readme",
            "Accept": "text/html",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.text


def parse(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    tips = {}
    for tip in soup.find_all("tool-tip"):
        target = tip.get("for")
        if target:
            tips[target] = tip.get_text(" ", strip=True)

    days = []
    for cell in soup.select("td.ContributionCalendar-day[data-date]"):
        ident = cell.get("id") or ""
        found = CELL_ID.search(ident)
        if not found:
            continue
        level = int(cell.get("data-level") or 0)
        count = parse_count(tips.get(ident, ""), level)
        days.append(
            {
                "date": cell["data-date"],
                "count": count,
                "level": level,
                "row": int(found.group(1)),
                "col": int(found.group(2)),
            }
        )

    if not days:
        raise SystemExit("nenhuma célula de contribuição encontrada; o HTML do GitHub mudou.")

    days.sort(key=lambda item: item["date"])
    best = max(days, key=lambda item: (item["count"], item["date"]))
    months: dict[str, int] = defaultdict(int)
    for item in days:
        months[item["date"][:7]] += item["count"]

    reported = None
    heading = soup.select_one("h2")
    if heading:
        match = REPORTED.search(heading.get_text(" ", strip=True))
        if match:
            reported = int(match.group(1).replace(",", ""))

    total = sum(item["count"] for item in days)
    payload = {
        "username": USERNAME,
        "total": total,
        "reported_total": reported,
        "from": days[0]["date"],
        "to": days[-1]["date"],
        "current_streak": current_streak(days),
        "longest_streak": longest_streak(days),
        "best_day": (
            None
            if best["count"] == 0
            else {"date": best["date"], "count": best["count"]}
        ),
        "months": [{"month": key, "count": months[key]} for key in sorted(months)],
        "days": days,
    }
    if reported is not None and reported != total:
        print(f"aviso: soma dos dias={total}, título da página={reported}")
    return payload


def main() -> None:
    payload = parse(fetch_html())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"{OUT} total={payload['total']} "
        f"streak={payload['current_streak']} "
        f"longest={payload['longest_streak']}"
    )


if __name__ == "__main__":
    main()

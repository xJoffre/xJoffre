import datetime
import json
import os
import sys
import urllib.request
from pathlib import Path

from receipt import FONT, LEFT, RIGHT, SIZES, THEMES, Receipt

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar { totalContributions weeks { contributionDays { date contributionLevel } } }
    }
  }
}
"""
MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
LEVELS = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
DOT_RADII = (0.9, 1.6, 2.3, 3.0, 3.7)
EMPTY_OPACITY = ".35"


def fetch(login, token):
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request) as response:
        payload = json.load(response)
    if "errors" in payload:
        raise SystemExit(f"GraphQL: {payload['errors']}")
    return payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def dot(colors, x, y, level):
    opacity = "1" if level else EMPTY_OPACITY
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{DOT_RADII[level]}" fill="{colors["ink"]}" opacity="{opacity}"/>'


def month_labels(colors, weeks, step, y):
    labels, previous = "", None
    for i, week in enumerate(weeks[:-2]):
        month = datetime.date.fromisoformat(week[0]["date"]).month
        if month != previous:
            labels += f'<text x="{LEFT + i * step:.1f}" y="{y}" style="{FONT};font-size:{SIZES["month"]}px" fill="{colors["note"]}">{MONTHS[month - 1]}</text>'
            previous = month
    return labels


def grid(colors, weeks, step, top):
    dots = ""
    for i, week in enumerate(weeks):
        for day in week:
            row = datetime.date.fromisoformat(day["date"]).isoweekday() % 7
            dots += dot(colors, LEFT + (i + .5) * step, top + (row + .5) * step, LEVELS[day["contributionLevel"]])
    return dots


def legend(colors, y):
    x = LEFT + 62
    dots = "".join(dot(colors, x + level * 14, y - 4, level) for level in range(len(DOT_RADII)))
    caption = f'style="{FONT};font-size:{SIZES["legend"]}px" fill="{colors["note"]}"'
    return f'<text x="{LEFT}" y="{y}" {caption}>menos</text>{dots}<text x="{x + len(DOT_RADII) * 14}" y="{y}" {caption}>más</text>'


def ticket(colors, login, calendar, printed):
    weeks = [week["contributionDays"] for week in calendar["weeks"]]
    total = calendar["totalContributions"]
    step = (RIGHT - LEFT) / len(weeks)
    sheet = Receipt(colors)
    sheet.center("GRÁFICO IMPRESO", SIZES["title"], 700, 30)
    sheet.center(f"github.com/{login}", SIZES["small"])
    sheet.center(f"Impreso: {printed.day:02d} {MONTHS[printed.month - 1]} {printed.year}, {printed:%H:%M} UTC", SIZES["small"], gap=30)
    sheet.rule()
    sheet.draw(month_labels(colors, weeks, step, sheet.y), 12)
    sheet.draw(grid(colors, weeks, step, sheet.y), 7 * step + 22)
    sheet.draw(legend(colors, sheet.y), 26)
    sheet.rule()
    sheet.pair("TOTAL", f"{total} {'contribución' if total == 1 else 'contribuciones'}", SIZES["total"], 700)
    sheet.rule()
    sheet.center("Se imprime de nuevo cada día", SIZES["small"], gap=18)
    sheet.barcode(printed.date().isoformat())
    sheet.center(printed.date().isoformat(), SIZES["caption"], gap=30)
    return sheet.render(f"Gráfico de contribuciones de {login} impreso en puntos: {total} contribuciones en el último año.")


def main():
    login, out_dir = sys.argv[1], Path(sys.argv[2])
    calendar = fetch(login, os.environ["GITHUB_TOKEN"])
    printed = datetime.datetime.now(datetime.timezone.utc)
    out_dir.mkdir(parents=True, exist_ok=True)
    for theme, colors in THEMES.items():
        (out_dir / f"activity-{theme}.svg").write_text(ticket(colors, login, calendar, printed), encoding="utf-8", newline="\n")


main()

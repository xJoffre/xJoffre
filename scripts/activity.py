import datetime
import json
import os
import sys
import urllib.request
from pathlib import Path

from receipt import SIZES, THEMES, Receipt

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalPullRequestReviewContributions
      restrictedContributionsCount
      contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } }
    }
  }
}
"""
WEEKDAYS = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]
MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


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
    return payload["data"]["user"]["contributionsCollection"]


def day_label(date):
    return f"{WEEKDAYS[date.weekday()]} {date.day:02d} {MONTHS[date.month - 1]}"


def streaks(days):
    longest = run = 0
    for _date, count in days:
        run = run + 1 if count else 0
        longest = max(longest, run)
    counts = [count for _date, count in days]
    if counts and counts[-1] == 0:
        counts.pop()
    current = 0
    for count in reversed(counts):
        if not count:
            break
        current += 1
    return current, longest


def plural(number, one, many):
    return f"{number} {one if number == 1 else many}"


def ticket(colors, login, stats, days, printed):
    current, longest = streaks(days)
    busiest_date, busiest_count = max(days, key=lambda day: day[1])
    sheet = Receipt(colors)
    sheet.center("ACTIVIDAD EN GITHUB", SIZES["title"], 700, 30)
    sheet.center(f"github.com/{login}", SIZES["small"])
    sheet.center(f"Impreso: {printed.day:02d} {MONTHS[printed.month - 1]} {printed.year}, {printed:%H:%M} UTC", SIZES["small"], gap=30)
    sheet.rule()
    sheet.pair("ÚLTIMOS 7 DÍAS", "CONTRIB.", SIZES["small"], 700)
    for date, count in days[-7:]:
        sheet.pair(day_label(date), str(count))
    sheet.rule()
    sheet.pair("ÚLTIMO AÑO", size=SIZES["small"], weight=700)
    for label, key in (("Commits", "totalCommitContributions"), ("Pull requests", "totalPullRequestContributions"),
                       ("Issues", "totalIssueContributions"), ("Revisiones", "totalPullRequestReviewContributions"),
                       ("En repos privados", "restrictedContributionsCount")):
        if stats[key]:
            sheet.pair(label, str(stats[key]))
    sheet.pair("Racha actual", plural(current, "día", "días"))
    sheet.pair("Racha más larga", plural(longest, "día", "días"))
    sheet.pair("Día más activo", f"{day_label(busiest_date)} ({busiest_count})")
    sheet.rule()
    total = stats["contributionCalendar"]["totalContributions"]
    sheet.pair("TOTAL", plural(total, "contribución", "contribuciones"), SIZES["total"], 700)
    sheet.rule()
    sheet.center("Se imprime de nuevo cada día", SIZES["small"], gap=18)
    sheet.barcode(printed.date().isoformat())
    sheet.center(printed.date().isoformat(), SIZES["caption"], gap=30)
    return sheet.render(f"Actividad en GitHub de {login}: {total} contribuciones en el último año, racha actual de {current} días.")


def main():
    login, out_dir = sys.argv[1], Path(sys.argv[2])
    stats = fetch(login, os.environ["GITHUB_TOKEN"])
    days = [(datetime.date.fromisoformat(day["date"]), day["contributionCount"])
            for week in stats["contributionCalendar"]["weeks"] for day in week["contributionDays"]]
    printed = datetime.datetime.now(datetime.timezone.utc)
    out_dir.mkdir(parents=True, exist_ok=True)
    for theme, colors in THEMES.items():
        (out_dir / f"activity-{theme}.svg").write_text(ticket(colors, login, stats, days, printed), encoding="utf-8", newline="\n")


main()

import json
import os
from bs4 import BeautifulSoup
from datetime import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)

with open(os.path.join(repo_root, "assets", "contributions_raw.html"), "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f.read(), "lxml")

days = []
for td in soup.select("td.ContributionCalendar-day"):
    date = td.get("data-date")
    level = td.get("data-level")
    if date is None:
        continue
    count_text = td.get("aria-label") or ""
    days.append({
        "date": date,
        "level": int(level) if level is not None else 0,
        "label": count_text.strip(),
    })

days.sort(key=lambda d: d["date"])

# streaks
total = 0
cur_streak = 0
longest_streak = 0
tmp = 0
weekday_counts = [0]*7
for d in days:
    lvl = d["level"]
    if lvl > 0:
        tmp += 1
        longest_streak = max(longest_streak, tmp)
        wd = datetime.strptime(d["date"], "%Y-%m-%d").weekday()
        weekday_counts[wd] += 1
    else:
        tmp = 0

# current streak = count back from most recent day
for d in reversed(days):
    if d["level"] > 0:
        cur_streak += 1
    else:
        break

busiest_idx = weekday_counts.index(max(weekday_counts)) if any(weekday_counts) else 0
busiest_day = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][busiest_idx]

out = {
    "days": days,
    "current_streak": cur_streak,
    "longest_streak": longest_streak,
    "busiest_day": busiest_day,
}

with open(os.path.join(repo_root, "assets", "contributions.json"), "w") as f:
    json.dump(out, f, indent=2)

print(f"Parsed {len(days)} days. Current streak: {cur_streak}, Longest: {longest_streak}, Busiest: {busiest_day}")

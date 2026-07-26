import json
import os
from datetime import datetime, timedelta

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)

with open(os.path.join(repo_root, "assets", "contributions.json")) as f:
    data = json.load(f)

days = data["days"]
day_map = {d["date"]: d["level"] for d in days}

LEVELS = ["#1a1a2e", "#16537e", "#1c7ed6", "#4dabf7", "#a5d8ff"]
CELL = 11
GAP = 3
LEFT_PAD = 30
TOP_PAD = 20

start = datetime.strptime(days[0]["date"], "%Y-%m-%d")
end = datetime.strptime(days[-1]["date"], "%Y-%m-%d")

# align to Sunday-start weeks like GitHub does
start_sunday = start - timedelta(days=(start.weekday() + 1) % 7)

weeks = []
cur = start_sunday
while cur <= end:
    week = []
    for i in range(7):
        d = cur + timedelta(days=i)
        key = d.strftime("%Y-%m-%d")
        week.append((key, day_map.get(key, 0)))
    weeks.append(week)
    cur += timedelta(days=7)

width = LEFT_PAD + len(weeks) * (CELL + GAP) + 20
height = TOP_PAD + 7 * (CELL + GAP) + 60

svg_parts = []
svg_parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
svg_parts.append(f'''
<style>
  .bg {{ fill: #0d1117; }}
  .cell {{ opacity: 0; }}
  .lbl {{ font-family: 'SFMono-Regular', Consolas, monospace; fill: #8b949e; font-size: 10px; }}
  .title {{ font-family: 'SFMono-Regular', Consolas, monospace; fill: #c9d1d9; font-size: 12px; }}
</style>
<rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="6"/>
''')

for wi, week in enumerate(weeks):
    for di, (date, level) in enumerate(week):
        x = LEFT_PAD + wi * (CELL + GAP)
        y = TOP_PAD + di * (CELL + GAP)
        color = LEVELS[min(level, 4)]
        delay = wi * 0.012
        svg_parts.append(
            f'<rect class="cell" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{color}">'
            f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.25s" fill="freeze"/>'
            f'</rect>'
        )

# legend
legend_y = height - 38
svg_parts.append(f'<text class="lbl" x="{LEFT_PAD}" y="{legend_y}">Less</text>')
lx = LEFT_PAD + 34
for lvl, color in enumerate(LEVELS):
    svg_parts.append(f'<rect x="{lx}" y="{legend_y-9}" width="{CELL}" height="{CELL}" rx="2" fill="{color}"/>')
    lx += CELL + GAP
svg_parts.append(f'<text class="lbl" x="{lx+4}" y="{legend_y}">More</text>')

# stats line
stats_y = height - 16
stats = f"{data['current_streak']}d current streak   ·   {data['longest_streak']}d longest streak   ·   busiest: {data['busiest_day']}"
svg_parts.append(f'<text class="title" x="{LEFT_PAD}" y="{stats_y}">{stats}</text>')

svg_parts.append('</svg>')

out_path = os.path.join(repo_root, "graph.svg")
with open(out_path, "w") as f:
    f.write("\n".join(svg_parts))

print(f"wrote {out_path}")

import os

ROWS = [
    ("role", "Backend Engineer"),
    ("stack", "Java 21 · Spring Boot · PostgreSQL · AWS"),
    ("focus", "Microservices, auth systems, AI-integrated backends"),
    ("now", "Job searching — Java backend roles, Noida/Delhi NCR"),
]

W, H = 460, 200
LINE_H = 26
TOP_PAD = 46
LEFT_PAD = 20

svg = []
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">')
svg.append(f'''
<style>
  .panel-bg {{ fill: #0d1117; stroke: #30363d; stroke-width: 1; }}
  .bar {{ fill: #161b22; }}
  .dot {{ opacity: 0.9; }}
  .key {{ font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px; fill: #58a6ff; opacity: 0; }}
  .val {{ font-family: 'SFMono-Regular', Consolas, monospace; font-size: 13px; fill: #c9d1d9; opacity: 0; }}
  .title {{ font-family: 'SFMono-Regular', Consolas, monospace; font-size: 12px; fill: #8b949e; }}
</style>
<rect class="panel-bg" x="1" y="1" width="{W-2}" height="{H-2}" rx="8"/>
<rect class="bar" x="1" y="1" width="{W-2}" height="28" rx="8"/>
<rect x="1" y="21" width="{W-2}" height="8" fill="#161b22"/>
<circle class="dot" cx="18" cy="15" r="5" fill="#ff5f56"/>
<circle class="dot" cx="34" cy="15" r="5" fill="#ffbd2e"/>
<circle class="dot" cx="50" cy="15" r="5" fill="#27c93f"/>
<text class="title" x="{W/2}" y="19" text-anchor="middle">sysinfo.sh</text>
''')

for i, (key, val) in enumerate(ROWS):
    y = TOP_PAD + i * LINE_H
    delay = 0.3 + i * 0.35
    svg.append(f'<text class="key" x="{LEFT_PAD}" y="{y}">{key}:<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.15s" fill="freeze"/></text>')
    svg.append(f'<text class="val" x="{LEFT_PAD+70}" y="{y}">{val}<animate attributeName="opacity" from="0" to="1" begin="{delay+0.1:.2f}s" dur="0.2s" fill="freeze"/></text>')

svg.append('</svg>')

script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)
out_path = os.path.join(repo_root, "sysinfo.svg")
with open(out_path, "w") as f:
    f.write("\n".join(svg))

print(f"wrote {out_path}")

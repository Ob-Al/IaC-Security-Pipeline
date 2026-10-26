import argparse
import html
import json
from pathlib import Path

COLORS = {"CRITICAL": "#b42318", "HIGH": "#e8590c", "MEDIUM": "#d4a106", "LOW": "#3b82f6", "UNKNOWN": "#868e96"}

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IaC Scan History</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
body {{ font-family: system-ui, sans-serif; margin: 0 auto; max-width: 1000px; padding: 24px 16px; color: #1f2328; }}
h1 {{ font-size: 22px; margin: 0 0 4px; }}
.sub {{ color: #656d76; margin-bottom: 24px; }}
.tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px; margin-bottom: 24px; }}
.tile {{ border: 1px solid #d0d7de; border-radius: 8px; padding: 12px; }}
.tile b {{ display: block; font-size: 24px; }}
table {{ width: 100%; border-collapse: collapse; font-size: 14px; margin-top: 24px; }}
th, td {{ text-align: left; padding: 6px 8px; border-bottom: 1px solid #eaeef2; }}
.sev {{ font-weight: 600; }}
.wrap {{ overflow-x: auto; }}
</style>
</head>
<body>
<h1>IaC scan history</h1>
<div class="sub">{runs} runs &middot; latest {latest_ts} on {latest_ref} ({latest_commit})</div>
<div class="tiles">{tiles}</div>
<canvas id="trend" height="110"></canvas>
<h2>Latest findings</h2>
<div class="wrap"><table>
<tr><th>severity</th><th>tool</th><th>rule</th><th>resource</th><th>location</th></tr>
{rows}
</table></div>
<script>
const data = {chart_data};
new Chart(document.getElementById("trend"), {{
  type: "line",
  data: {{
    labels: data.labels,
    datasets: data.series.map(s => ({{ label: s.name, data: s.values, borderColor: s.color, backgroundColor: s.color, tension: 0.2 }}))
  }},
  options: {{ scales: {{ y: {{ beginAtZero: true, ticks: {{ precision: 0 }} }} }} }}
}});
</script>
</body>
</html>
"""


def load_history(path):
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text().splitlines() if line.strip()]


def render(history, last_n=50):
    history = history[-last_n:]
    latest = history[-1]
    sevs = [s for s in COLORS if any(r["by_severity"].get(s) for r in history)] or ["HIGH"]

    chart = {
        "labels": [f"{r['timestamp'][:10]} {r['commit']}" for r in history],
        "series": [
            {"name": s, "color": COLORS[s], "values": [r["by_severity"].get(s, 0) for r in history]}
            for s in sevs
        ],
    }
    tiles = "".join(
        f'<div class="tile">{s.lower()}<b style="color:{COLORS[s]}">{n}</b></div>'
        for s, n in latest["by_severity"].items()
    )
    rows = "\n".join(
        "<tr>"
        f'<td class="sev" style="color:{COLORS[f["severity"]]}">{f["severity"]}</td>'
        f'<td>{html.escape(f["tool"])}</td><td>{html.escape(f["rule"])}</td>'
        f'<td>{html.escape(f["resource"])}</td><td>{html.escape(f["file"])}:{f["line"]}</td>'
        "</tr>"
        for f in sorted(latest["findings"], key=lambda f: list(COLORS).index(f["severity"]))
    ) or '<tr><td colspan="5">No findings</td></tr>'

    return PAGE.format(
        runs=len(history),
        latest_ts=latest["timestamp"],
        latest_ref=html.escape(latest["ref"]),
        latest_commit=html.escape(latest["commit"]),
        tiles=tiles,
        rows=rows,
        chart_data=json.dumps(chart),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--history", default="results/history.jsonl")
    ap.add_argument("--out", default="dashboard/index.html")
    args = ap.parse_args()

    history = load_history(args.history)
    if not history:
        raise SystemExit("no scan history yet")
    Path(args.out).write_text(render(history))
    print(f"wrote {args.out} from {len(history)} runs")


if __name__ == "__main__":
    main()

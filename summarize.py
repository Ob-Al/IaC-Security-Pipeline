import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SEVERITIES = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"]


def norm_sev(s, default="UNKNOWN"):
    s = (s or "").upper()
    return s if s in SEVERITIES else default


def parse_checkov(data, unknown_as="HIGH"):
    reports = data if isinstance(data, list) else [data]
    findings = []
    for report in reports:
        for c in report.get("results", {}).get("failed_checks", []):
            findings.append({
                "tool": "checkov",
                "rule": c["check_id"],
                "severity": norm_sev(c.get("severity"), unknown_as),
                "title": c.get("check_name", ""),
                "resource": c.get("resource", ""),
                "file": c.get("file_path", "").lstrip("/"),
                "line": (c.get("file_line_range") or [0])[0],
            })
    return findings


def parse_tfsec(data):
    findings = []
    for r in data.get("results") or []:
        loc = r.get("location", {})
        findings.append({
            "tool": "tfsec",
            "rule": r.get("long_id") or r.get("rule_id", ""),
            "severity": norm_sev(r.get("severity")),
            "title": r.get("description", ""),
            "resource": r.get("resource", ""),
            "file": os.path.relpath(loc["filename"]) if loc.get("filename") else "",
            "line": loc.get("start_line", 0),
        })
    return findings


def dedupe(findings):
    seen, out = set(), []
    for f in findings:
        key = (f["tool"], f["rule"], f["resource"], f["file"], f["line"])
        if key not in seen:
            seen.add(key)
            out.append(f)
    return out


def build_record(findings, sha=None, ref=None):
    counts = Counter(f["severity"] for f in findings)
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "commit": sha or os.getenv("GITHUB_SHA", "local")[:7],
        "ref": ref or os.getenv("GITHUB_REF_NAME", "local"),
        "total": len(findings),
        "by_severity": {s: counts.get(s, 0) for s in SEVERITIES},
        "by_tool": dict(Counter(f["tool"] for f in findings)),
        "findings": findings,
    }


def to_markdown(rec):
    lines = [f"### IaC scan: {rec['total']} findings", "", "| severity | count |", "|---|---|"]
    lines += [f"| {s} | {n} |" for s, n in rec["by_severity"].items() if n]
    if rec["findings"]:
        lines += ["", "| sev | tool | rule | resource | location |", "|---|---|---|---|---|"]
        order = {s: i for i, s in enumerate(SEVERITIES)}
        for f in sorted(rec["findings"], key=lambda f: order[f["severity"]])[:50]:
            lines.append(f"| {f['severity']} | {f['tool']} | {f['rule']} | {f['resource']} | {f['file']}:{f['line']} |")
    return "\n".join(lines) + "\n"


def should_fail(rec, fail_on):
    blocking = SEVERITIES[: SEVERITIES.index(fail_on) + 1]
    return sum(rec["by_severity"][s] for s in blocking) > 0


def load_json(path):
    p = Path(path)
    if not p.exists() or p.stat().st_size == 0:
        return None
    return json.loads(p.read_text())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkov", default="results/results_json.json")
    ap.add_argument("--tfsec", default="results/tfsec.json")
    ap.add_argument("--history", default="results/history.jsonl")
    ap.add_argument("--summary", default="results/summary.md")
    ap.add_argument("--fail-on", default="HIGH", choices=SEVERITIES[:4])
    ap.add_argument("--unknown-as", default="HIGH", choices=SEVERITIES)
    ap.add_argument("--no-gate", action="store_true")
    args = ap.parse_args()

    findings = []
    if (ck := load_json(args.checkov)) is not None:
        findings += parse_checkov(ck, args.unknown_as)
    if (tf := load_json(args.tfsec)) is not None:
        findings += parse_tfsec(tf)

    rec = build_record(dedupe(findings))
    Path(args.summary).parent.mkdir(parents=True, exist_ok=True)
    Path(args.summary).write_text(to_markdown(rec))
    with open(args.history, "a") as f:
        f.write(json.dumps(rec) + "\n")

    print(to_markdown(rec))
    if not args.no_gate and should_fail(rec, args.fail_on):
        print(f"failing: findings at or above {args.fail_on}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

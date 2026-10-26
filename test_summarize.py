import json
from pathlib import Path

from scripts.summarize import build_record, dedupe, parse_checkov, parse_tfsec, should_fail, to_markdown

FIX = Path(__file__).parent / "fixtures"


def load(name):
    return json.loads((FIX / name).read_text())


def test_parse_checkov():
    findings = parse_checkov(load("checkov.json"))
    assert [f["rule"] for f in findings] == ["CKV2_ORG_3", "CKV_AWS_17"]
    assert findings[0]["severity"] == "CRITICAL"
    assert findings[0]["file"] == "main.tf"
    assert findings[0]["line"] == 37


def test_null_severity_uses_fallback():
    assert parse_checkov(load("checkov.json"))[1]["severity"] == "HIGH"
    assert parse_checkov(load("checkov.json"), unknown_as="LOW")[1]["severity"] == "LOW"


def test_checkov_list_output():
    data = [load("checkov.json"), {"check_type": "secrets", "results": {"failed_checks": []}}]
    assert len(parse_checkov(data)) == 2


def test_parse_tfsec():
    findings = parse_tfsec(load("tfsec.json"))
    assert findings[0]["rule"] == "aws-ec2-no-public-ingress-sgr"
    assert {f["severity"] for f in findings} == {"CRITICAL", "MEDIUM"}


def test_tfsec_null_results():
    assert parse_tfsec({"results": None}) == []


def test_dedupe():
    f = parse_tfsec(load("tfsec.json"))
    assert len(dedupe(f + f)) == 2


def test_gate():
    rec = build_record(parse_tfsec(load("tfsec.json")), sha="abc", ref="main")
    assert should_fail(rec, "HIGH")
    assert should_fail(rec, "CRITICAL")

    medium_only = build_record([f for f in parse_tfsec(load("tfsec.json")) if f["severity"] == "MEDIUM"])
    assert not should_fail(medium_only, "HIGH")
    assert should_fail(medium_only, "MEDIUM")


def test_markdown_sorted_by_severity():
    rec = build_record(parse_tfsec(load("tfsec.json"))[::-1])
    md = to_markdown(rec)
    assert md.index("CRITICAL | tfsec") < md.index("MEDIUM | tfsec")

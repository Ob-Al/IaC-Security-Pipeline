import pytest

pytest.importorskip("checkov")

from checkov.common.models.enums import CheckResult

from policies.checkov.public_ingress import check


def sg(*rules):
    return {"ingress": list(rules)}


def rule(lo, hi, cidr="0.0.0.0/0", proto="tcp"):
    return {"from_port": [lo], "to_port": [hi], "protocol": [proto], "cidr_blocks": [[cidr]]}


@pytest.mark.parametrize("conf,expected", [
    (sg(rule(443, 443)), CheckResult.PASSED),
    (sg(rule(80, 80), rule(443, 443)), CheckResult.PASSED),
    (sg(rule(22, 22)), CheckResult.FAILED),
    (sg(rule(22, 22, cidr="10.0.0.0/8")), CheckResult.PASSED),
    (sg(rule(80, 443)), CheckResult.FAILED),
    (sg(rule(0, 0, proto="-1")), CheckResult.FAILED),
    (sg({"from_port": [5432], "to_port": [5432], "protocol": ["tcp"], "ipv6_cidr_blocks": [["::/0"]]}), CheckResult.FAILED),
])
def test_security_group(conf, expected):
    assert check.scan_resource_conf(conf) == expected


def test_standalone_rule():
    conf = {"type": ["ingress"], "from_port": [3306], "to_port": [3306], "protocol": ["tcp"], "cidr_blocks": [["0.0.0.0/0"]]}
    assert check.scan_resource_conf(conf) == CheckResult.FAILED
    conf["type"] = ["egress"]
    assert check.scan_resource_conf(conf) == CheckResult.PASSED


def test_dashboard_renders(tmp_path):
    from dashboard.build import render
    rec = {"timestamp": "2026-10-25T12:00:00+00:00", "commit": "abc1234", "ref": "main", "total": 1,
           "by_severity": {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 0, "LOW": 0, "UNKNOWN": 0},
           "findings": [{"severity": "HIGH", "tool": "checkov", "rule": "X", "resource": "<script>", "file": "a.tf", "line": 1}]}
    page = render([rec, rec])
    assert "2 runs" in page
    assert "&lt;script&gt;" in page

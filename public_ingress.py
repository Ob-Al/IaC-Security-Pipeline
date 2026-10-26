from checkov.common.models.enums import CheckCategories, CheckResult
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck

ALLOWED_PUBLIC_PORTS = {80, 443}
PUBLIC = {"0.0.0.0/0", "::/0"}


def first(v, default=None):
    if isinstance(v, list):
        return v[0] if v else default
    return v if v is not None else default


def is_bad_rule(rule):
    cidrs = set(first(rule.get("cidr_blocks"), []) or []) | set(first(rule.get("ipv6_cidr_blocks"), []) or [])
    if not cidrs & PUBLIC:
        return False
    try:
        lo, hi = int(first(rule.get("from_port"), 0)), int(first(rule.get("to_port"), 0))
    except (TypeError, ValueError):
        return True
    if str(first(rule.get("protocol"), "")) == "-1":
        return True
    return not set(range(lo, hi + 1)) <= ALLOWED_PUBLIC_PORTS


class NoPublicIngressExceptWeb(BaseResourceCheck):
    def __init__(self):
        super().__init__(
            name="Only ports 80 and 443 may be open to the internet",
            id="CKV_ORG_4",
            categories=[CheckCategories.NETWORKING],
            supported_resources=["aws_security_group", "aws_security_group_rule"],
        )

    def scan_resource_conf(self, conf):
        if "type" in conf:
            if first(conf["type"]) != "ingress":
                return CheckResult.PASSED
            return CheckResult.FAILED if is_bad_rule(conf) else CheckResult.PASSED

        for rule in conf.get("ingress", []):
            if isinstance(rule, dict) and is_bad_rule(rule):
                return CheckResult.FAILED
        return CheckResult.PASSED


check = NoPublicIngressExceptWeb()

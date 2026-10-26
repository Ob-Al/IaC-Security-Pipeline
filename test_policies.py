import json
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
CUSTOM = {"CKV2_ORG_1", "CKV2_ORG_2", "CKV2_ORG_3", "CKV_ORG_4"}

pytestmark = pytest.mark.skipif(not shutil.which("checkov"), reason="checkov not installed")


def failed_ids(path):
    out = subprocess.run(
        ["checkov", "-d", path, "--config-file", ".checkov.yaml", "-o", "json", "--quiet", "--soft-fail"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    )
    data = json.loads(out.stdout)
    reports = data if isinstance(data, list) else [data]
    return {c["check_id"] for r in reports for c in r.get("results", {}).get("failed_checks", [])}


def test_custom_policies_catch_insecure_example():
    assert CUSTOM <= failed_ids("examples/insecure")


def test_main_stack_is_clean():
    assert failed_ids("terraform") == set()

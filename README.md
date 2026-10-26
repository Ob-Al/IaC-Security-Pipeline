# IaC Security Pipeline

CI pipeline that scans Terraform before it gets deployed. Runs Checkov and tfsec with custom org policies on every PR, blocks merges on high/critical findings, and publishes a dashboard that tracks results over time.

```
PR -> fmt/validate -> checkov + tfsec (default + custom rules)
   -> SARIF to GitHub code scanning
   -> summary comment on the PR
   -> gate: fail on HIGH or above
main -> append to history -> rebuild dashboard on gh-pages
```

## Layout

| path | what |
|---|---|
| `terraform/` | the stack being protected (S3, KMS, VPC, flow logs, bastion SG) |
| `examples/insecure/` | intentionally bad config used to prove the rules fire |
| `policies/checkov/` | custom Checkov policies (YAML + one Python check) |
| `.tfsec/` | custom tfsec checks |
| `.checkov.yaml` | Checkov config and documented suppressions |
| `scripts/scan.sh` | runs everything, same locally and in CI |
| `scripts/summarize.py` | merges both scanners into one result, writes history, applies the gate |
| `dashboard/build.py` | static HTML dashboard from scan history |
| `.github/workflows/iac-security.yml` | the pipeline |

## Custom rules

Default rulesets cover generic misconfigurations. These cover org-specific policy:

| id | rule | severity |
|---|---|---|
| CKV2_ORG_1 | owner and environment tags required | MEDIUM |
| CKV2_ORG_2 | EC2 limited to approved instance families (t3, t3a, m6i) | HIGH |
| CKV2_ORG_3 | RDS must use a Secrets Manager managed password | CRITICAL |
| CKV_ORG_4 | only 80/443 can be open to 0.0.0.0/0 or ::/0 (defaults only check specific ports) | HIGH |
| ORG001 (tfsec) | owner tag required | MEDIUM |
| ORG002 (tfsec) | RDS can't be publicly accessible | CRITICAL |

## Run locally

```bash
pip install checkov pytest
./scripts/scan.sh terraform
./scripts/scan.sh examples/insecure --history /dev/null
pytest
```

Or with Docker, no local installs:

```bash
docker build -t iac-scan .
docker run --rm -v "$PWD:/repo" iac-scan terraform
```

## Severity handling

Open-source Checkov doesn't return severities for built-in checks without a Prisma Cloud key. Those come back as null and get treated as HIGH by default (`--unknown-as`), so nothing slips through just because it's unrated. Custom policies set their own severity.

## Suppressions

Skips live in `.checkov.yaml` or inline `#checkov:skip=ID:reason`, always with a reason, so they show up in code review.

## Dashboard

On every push to main, the latest result is appended to `history.jsonl` on the `gh-pages` branch and `index.html` is rebuilt. Enable GitHub Pages from that branch to view it.

## Notes

- tfsec has been folded into Trivy (`trivy config`). The custom-check approach carries over; switching is mostly a CLI change.
- Next steps: OPA/Conftest on `terraform plan` JSON to catch things only known at plan time, and drift detection on a schedule.

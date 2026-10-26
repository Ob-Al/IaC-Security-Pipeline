### IaC scan: 44 findings

| severity | count |
|---|---|
| CRITICAL | 1 |
| HIGH | 39 |
| MEDIUM | 4 |

| sev | tool | rule | resource | location |
|---|---|---|---|---|
| CRITICAL | checkov | CKV2_ORG_3 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_24 | aws_security_group.open | main.tf:10 |
| HIGH | checkov | CKV_AWS_260 | aws_security_group.open | main.tf:10 |
| HIGH | checkov | CKV_AWS_277 | aws_security_group.open | main.tf:10 |
| HIGH | checkov | CKV_AWS_23 | aws_security_group.open | main.tf:10 |
| HIGH | checkov | CKV_AWS_25 | aws_security_group.open | main.tf:10 |
| HIGH | checkov | CKV_ORG_4 | aws_security_group.open | main.tf:10 |
| HIGH | checkov | CKV_AWS_79 | aws_instance.big | main.tf:29 |
| HIGH | checkov | CKV_AWS_135 | aws_instance.big | main.tf:29 |
| HIGH | checkov | CKV_AWS_8 | aws_instance.big | main.tf:29 |
| HIGH | checkov | CKV_AWS_126 | aws_instance.big | main.tf:29 |
| HIGH | checkov | CKV_AWS_16 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_293 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_17 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_157 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_353 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_118 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_226 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_129 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_161 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_286 | aws_iam_policy.admin | main.tf:48 |
| HIGH | checkov | CKV_AWS_290 | aws_iam_policy.admin | main.tf:48 |
| HIGH | checkov | CKV_AWS_288 | aws_iam_policy.admin | main.tf:48 |
| HIGH | checkov | CKV_AWS_62 | aws_iam_policy.admin | main.tf:48 |
| HIGH | checkov | CKV_AWS_289 | aws_iam_policy.admin | main.tf:48 |
| HIGH | checkov | CKV_AWS_287 | aws_iam_policy.admin | main.tf:48 |
| HIGH | checkov | CKV_AWS_63 | aws_iam_policy.admin | main.tf:48 |
| HIGH | checkov | CKV_AWS_355 | aws_iam_policy.admin | main.tf:48 |
| HIGH | checkov | CKV2_ORG_2 | aws_instance.big | main.tf:29 |
| HIGH | checkov | CKV2_AWS_60 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV2_AWS_6 | aws_s3_bucket.public | main.tf:1 |
| HIGH | checkov | CKV2_AWS_41 | aws_instance.big | main.tf:29 |
| HIGH | checkov | CKV2_AWS_61 | aws_s3_bucket.public | main.tf:1 |
| HIGH | checkov | CKV2_AWS_30 | aws_db_instance.db | main.tf:37 |
| HIGH | checkov | CKV_AWS_18 | aws_s3_bucket.public | main.tf:1 |
| HIGH | checkov | CKV2_AWS_5 | aws_security_group.open | main.tf:10 |
| HIGH | checkov | CKV2_AWS_40 | aws_iam_policy.admin | main.tf:48 |
| HIGH | checkov | CKV_AWS_20 | aws_s3_bucket.public | main.tf:1 |
| HIGH | checkov | CKV_AWS_21 | aws_s3_bucket.public | main.tf:1 |
| HIGH | checkov | CKV_AWS_145 | aws_s3_bucket.public | main.tf:1 |
| MEDIUM | checkov | CKV2_ORG_1 | aws_s3_bucket.public | main.tf:1 |
| MEDIUM | checkov | CKV2_ORG_1 | aws_security_group.open | main.tf:10 |
| MEDIUM | checkov | CKV2_ORG_1 | aws_instance.big | main.tf:29 |
| MEDIUM | checkov | CKV2_ORG_1 | aws_db_instance.db | main.tf:37 |

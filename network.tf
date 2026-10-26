resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  tags                 = merge(local.tags, { Name = "${var.environment}-vpc" })
}

resource "aws_default_security_group" "default" {
  vpc_id = aws_vpc.main.id
  tags   = local.tags
}

resource "aws_cloudwatch_log_group" "flow" {
  name              = "/vpc/${var.environment}/flow-logs"
  retention_in_days = 365
  kms_key_id        = aws_kms_key.data.arn
  tags              = local.tags
}

resource "aws_iam_role" "flow" {
  name = "${var.environment}-vpc-flow-logs"
  tags = local.tags
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "vpc-flow-logs.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "flow" {
  role = aws_iam_role.flow.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect   = "Allow"
      Action   = ["logs:CreateLogStream", "logs:PutLogEvents", "logs:DescribeLogStreams"]
      Resource = "${aws_cloudwatch_log_group.flow.arn}:*"
    }]
  })
}

resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  log_destination = aws_cloudwatch_log_group.flow.arn
  iam_role_arn    = aws_iam_role.flow.arn
  tags            = local.tags
}

resource "aws_security_group" "bastion" {
  #checkov:skip=CKV2_AWS_5:attached to the bastion instance in the compute stack
  name        = "${var.environment}-bastion"
  description = "SSH from admin network only"
  vpc_id      = aws_vpc.main.id
  tags        = local.tags

  ingress {
    description = "ssh from admin cidr"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.admin_cidr]
  }

  egress {
    description = "https out"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
}

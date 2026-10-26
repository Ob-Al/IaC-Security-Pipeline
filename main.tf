terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
  default_tags {
    tags = local.tags
  }
}

locals {
  tags = {
    owner       = var.owner
    environment = var.environment
    project     = "iac-security-pipeline"
  }
}

data "aws_caller_identity" "current" {}

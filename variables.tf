variable "region" {
  type    = string
  default = "us-east-1"
}

variable "owner" {
  type = string
}

variable "environment" {
  type    = string
  default = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod"
  }
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}

variable "admin_cidr" {
  type        = string
  description = "CIDR allowed to reach the bastion over SSH"
}

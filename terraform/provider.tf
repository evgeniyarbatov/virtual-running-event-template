provider "aws" {
  region = local.config.aws_region
}

data "aws_region" "current" {}

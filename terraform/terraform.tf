terraform {
  backend "s3" {
    encrypt      = true
    bucket       = "arbatov-terraform-state"
    use_lockfile = true
    key          = "virtual-running-event-template.tfstate"
    region       = "ap-southeast-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

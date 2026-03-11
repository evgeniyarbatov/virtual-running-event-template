variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "s3_bucket" {
  type    = string
  default = "vr-run.example.com" # Name of S3 bucket should match Cloudflare DNS name
}

variable "s3_bucket_dir" {
  type    = string
  default = "../site/dist"
}

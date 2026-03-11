variable "aws_region" {
  type = string
}

variable "s3_bucket" {
  type = string
}

variable "s3_bucket_dir" {
  type = string
}

variable "event_country" {
  type = string
}

variable "event_title" {
  type = string
}

variable "event_subtitle" {
  type = string
}

variable "event_custom_texts" {
  type = list(string)
}

variable "event_start_point" {
  type = string
}

variable "event_stop_point" {
  type = string
}

resource "aws_s3_object" "static_files" {
  for_each = fileset(local.config.s3_bucket_dir, "**")

  bucket       = aws_s3_bucket.bucket.id
  key          = each.value
  source       = "${local.config.s3_bucket_dir}/${each.value}"
  content_type = lookup(local.content_types, regex("\\.[^.]+$", each.value), null)
  etag         = filemd5("${local.config.s3_bucket_dir}/${each.value}")
}

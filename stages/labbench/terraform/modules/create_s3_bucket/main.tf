

# create a bucket
data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "current" {

  bucket = "${var.bucket_name}-${var.parent_context.account_id}"

  tags = {
    Name        = var.bucket_name
    Description = var.description
    Environment = var.common_tags.Environment
    Creator  = var.common_tags.Creator
  }
}

resource "aws_s3_bucket_acl" "current" {
  bucket = aws_s3_bucket.current.id
  acl    = "private"
}

# block all public access to bucket

resource "aws_s3_bucket_public_access_block" "current_block_all" {
  bucket = aws_s3_bucket.current.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

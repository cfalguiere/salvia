# return bucket

output "current_bucket" {
  value       = aws_s3_bucket.current
  description = "Bucket Created"
}

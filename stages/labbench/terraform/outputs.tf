output "bucket_created" {
  value       = module.shared_s3_bucket.current_bucket
  description = "Bucket created"
}

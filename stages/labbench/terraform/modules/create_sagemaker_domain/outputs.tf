# return bucket

output "current_domain" {
  value       = aws_sagemaker_domain.current
  description = "Domain Created"
}

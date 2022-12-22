variable "bucket_name" {
  description = "the bucket name"
  type        = string
}

variable "description" {
  description = "the bucket description"
  type        = string
}

variable "ou_path" {
  description = "the path inside IAM names"
  type        = string
}


variable "parent_context" {
  description = "useful vars to share with the child module"
  type = object({
      account_id            = string
      region                = string
  })
}


variable "common_tags" {
  description = "common tags"
  type     = object({
    Environment = string
    Creator     = string
  })
}

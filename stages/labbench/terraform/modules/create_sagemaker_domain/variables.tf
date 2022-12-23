variable "domain_name" {
  description = "the domain name"
  type        = string
}

variable "description" {
  description = "the domain description"
  type        = string
}

variable "role_name" {
  description = "the default_user_settings role name"
  type        = string
}

variable "ou_path" {
  description = "the path inside IAM names"
  type        = string
}


variable "vpc" {
  description = "common tags"
  type     = object({
    id = string
  })
}


variable "parent_context" {
  description = "useful vars to share with the child module"
  type = object({
      account_id            = string
      region                = string
      platform              = string
      environment           = string
  })
}


variable "common_tags" {
  description = "common tags"
  type     = object({
    Environment = string
    Creator     = string
  })
}

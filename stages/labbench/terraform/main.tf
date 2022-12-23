# set the workbench with an admin role, a scheduled stop lambda

terraform {
  required_version = ">= 1.2.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 2.70.1"
    }
  }
  backend "s3" {}
}


data "aws_caller_identity" "current" {}


locals {
  # var passed to modules
  common_tags = {
    Environment = "${var.platform_label}-${var.environment_label}"
    Creator     = "SDI" # FIXME
    #Creator     = "SDI ${var.profile}"
  }
  parent_context = {
    account_id      = data.aws_caller_identity.current.account_id
    region          = var.region
    environment     = var.environment
    platform        = var.platform
  }
}


provider "aws" {
  region  = var.region
  shared_credentials_file = var.shared_credentials_file

  # require v3.38 or higher
  #default tags {
  #  tags = local.common_tags
  #}
}

/*
  sub modules
*/

# create a shared s3 bucket for sagemaker

module "shared_s3_bucket" {
  source = "./modules/create_s3_bucket"

  bucket_name = "salvia-${var.environment}-${var.region}"  # account id is added
  ou_path     = "/salvia/${var.environment}/"
  description = "A bucket for ${var.environment_label} experiments"

  parent_context =  local.parent_context
  common_tags = local.common_tags
}

# and create default folders

locals {
  names = toset(["data", "sdi", "work"])
}

resource "aws_s3_bucket_object" "base_folder" {
  for_each = local.names
  
  bucket  = module.shared_s3_bucket.current_bucket.id
  acl     = "private"
  key     =  each.value
  content_type = "application/x-directory"
}


# dump some configuration information onto S3

resource "aws_s3_bucket_object" "file_upload" {
  bucket      = module.shared_s3_bucket.current_bucket.id
  acl         = "private"
  key         = "env_configuration.json"
  content  = jsonencode({
    Domain = {
      Platform = var.platform,
      Environment = var.environment
    }
  })
  content_type = "application/json"
  #source      = local_file.env_configuration.filename

  # The filemd5() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the md5() function and the file() function:
  # etag = "${md5(file("path/to/file"))}"
  #etag        = filemd5(local_file.env_configuration.filename)
  
  #provisioner "local-exec" {
  #   command = "aws s3 cp ${local.object_source} ${module.shared_s3_bucket.current_bucket.uri}/"
  #}
}


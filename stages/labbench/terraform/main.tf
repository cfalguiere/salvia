# set the workbench with an admin role, a scheduled stop lambda

terraform {
  required_version = ">= 1.2.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 2.7"
    }
  }
  backend "s3" {}
}


data "aws_caller_identity" "current" {}


locals {
  # var passed to modules
  common_tags = {
    Environment = var.environment
    Creator     = "SDI" # FIXME
    #Creator     = "SDI ${var.profile}"
  }
  parent_context = {
    account_id      = data.aws_caller_identity.current.account_id
    region          = var.region
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

  bucket_name = "salvia-labbench-${var.region}" # account id is added
  ou_path     = "/salvia/labbench/"
  description = "A bucket for LabBench experiments"

  parent_context =  local.parent_context
  common_tags = local.common_tags
}

resource "aws_s3_bucket_object" "base_folder" {
    bucket  = "${module.shared_s3_bucket.current_bucket.id}"
    acl     = "private"
    key     =  "data/"
    content_type = "application/x-directory"
}


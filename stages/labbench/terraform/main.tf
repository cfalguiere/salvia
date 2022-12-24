# set the workbench with an admin role, a scheduled stop lambda

terraform {
  required_version = ">= 1.3.6"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      #version = "~> 2.70.1"
      version = "~> 4.48.0"
    }
    # workaround for schema missing - appeared with upgrade - FIXME
    local = {
      version = "~> 2.1"
    }

  }

  # storage for states
  backend "s3" {}
}



# configure the aws provider 

provider "aws" {
  region  = var.region

  # require v3.38 or higher
  #default tags {
  #  tags = local.common_tags
  #}
}


# initialise some  context

data "aws_caller_identity" "current" {}


resource "aws_default_vpc" "default" {
  tags = {
    Name = "Default VPC"
  }
}


# sets some common settings

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

resource "aws_s3_object" "base_folder" {
  for_each = local.names
  
  bucket  = module.shared_s3_bucket.current_bucket.id
  acl     = "private"
  key     =  each.value
  content_type = "application/x-directory"
}

# create the sagemaker domain
# does not work with preprovisionned terraform - requires anupgrade of the provixder and terraform

module "sagemaker_domain" {
  source = "./modules/create_sagemaker_domain"

  domain_name = "salvia-${var.environment}-${var.region}"
  role_name   = "salvia-${var.environment}-${var.region}"
  ou_path     = "/salvia/${var.environment}/"
  description = "A domain for ${var.environment_label} experiments"
  vpc         = aws_default_vpc.default
  
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sagemaker_domain
  # TODO other options

  parent_context =  local.parent_context
  common_tags = local.common_tags
}


# dump some configuration information onto S3

resource "aws_s3_object" "file_upload" {
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


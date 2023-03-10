

# create a domain

data "aws_subnets" "public" {
  filter {
    name   = "vpc-id"
    values = [var.vpc.id]
  }
}

resource "aws_sagemaker_domain" "current" {
  domain_name = var.domain_name
  auth_mode   = "IAM"
  vpc_id      = var.vpc.id
  subnet_ids  = data.aws_subnets.public.ids

  default_user_settings {
    execution_role = aws_iam_role.current.arn
  }
  
  #(Optional) The retention policy for data stored on an Amazon Elastic File System (EFS) volume. 
  #Valid values are Retain or Delete. Default value is Retain.
  retention_policy {
    home_efs_file_system = "Delete" # "Retain" "Delete"
  }
  
  # https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/sagemaker_domain
  # TODO other options

  tags = {
    Name        = var.domain_name
    Description = var.description
    Environment = var.common_tags.Environment
    Creator  = var.common_tags.Creator
  }

}

resource "aws_iam_role" "current" {
  name               = var.role_name
  path               = var.ou_path
  assume_role_policy = data.aws_iam_policy_document.current.json
  

  tags = {
    Name        = var.domain_name
    Description = var.description
    Environment = var.common_tags.Environment
    Creator  = var.common_tags.Creator
  }

}

data "aws_iam_policy_document" "current" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["sagemaker.amazonaws.com"]
    }
  }
}


data "aws_iam_policy" "s3full" {
  name = "AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "s3full" {
  role       = aws_iam_role.current.name
  policy_arn = data.aws_iam_policy.s3full.arn
}



data "aws_iam_policy" "smfull" {
  name = "AmazonSageMakerFullAccess"
}

resource "aws_iam_role_policy_attachment" "smfull" {
  role       = aws_iam_role.current.name
  policy_arn = data.aws_iam_policy.smfull.arn
}
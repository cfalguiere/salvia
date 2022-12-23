# salvia
AWS tests

# Introduction

Utilities to create AWS environments 

Leverages
- AWS
- Git
- Terraform


# Environments setup

This repository includes setups for several environments

## Environments and main features

| Name | Description | Features |
| LabBench | Quick setup for lab environments. | create an S3 bucket and a SageMaker Domain |


## Prerequisites

This is expected to be run from within the AWS account in Cloud9. 
It should run in another type of environment like an EC2 instance, or a local setup with AWS CLI configured.
Thise configuration are not tested though.

- setup a Cloud9 environment in the region you want to operate the environment
- setup the git configuration on this instance
- clone the repository

All the scripts leverage Terraform. It is preinstalled on Cloud9 environment. If you run a different setup you may want to install it.

As SageMaker studio features are new, youmust upgrade the terraform version preinstalled in Cloud9.
````
$ terraform init -upgrade
````

## Initialisation of LabBench

Two major steps
- generate the configuration. The script _terraform-configure.sh_ will collect information from the current context and yield configuration files. 
- run the terraform plan

You may find the configuration files generated under the terraform subfolder. 
Files are named *.generated.* so they may be ignored by git leveraging the .gitignore configuration.
These files are not kept in version control as they might include secrets (account id, access keys).

The script currenlty rely on the credentials provisionned by Cloud9. 
If you run this from a local workstation you may want to replace this with access key and secret key. 
Do not put these information in the script if you want to keep the script in version control.


*Instructions*
From the root of the repository
```
$ cd stages/labbench
$ ./terraform-configure.sh
$ cd terraform
$ terraform init -backend-config var-backend.generated.auto.tfvars
$ terraform validate
$ terraform  plan -out tfplan
$ terraform apply -auto-approve tfplan
```

## destroy an environment

Once you are fone with the environment you may destroy it. 
Please keep in mind that all resources created in SageMaker Domain and on S" will be lost

For instance to destroy the LabBench environment, floow instructions below:

```
$ cd stages/labbench/terraform
$ terraform destroy 
```

For more information refer to the Terraform page https://developer.hashicorp.com/terraform/cli/commands/destroy
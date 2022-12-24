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
These configuration are not tested though.

### Setup a Cloud9 instance

setup a Cloud9 environment in the region you want to operate the environment

### Setup Git on the Cloud Instance

configure the git credentials 


### Clone this repository onto the Cloud instance

### Upgrade Terraform on the Cloud9 instance

All the scripts leverage Terraform. It is preinstalled on Cloud9 environment. If you run a different setup you may want to install it.

As SageMaker studio features are new, youmust upgrade the terraform version preinstalled in Cloud9.
````
$ terraform init -upgrade
````

### Setup you credentials on the Cloud9 instance

Cloud9 allocate some credentials in the default location ~/.aws/credentials. These are temporary token that works for most services. 
However we want to be able to autorize additional services.

The terraform plan will use environment variable to hget access to the access key and secret key.

Open ~/.bashrec and add the lines below addapted for your configuration at the end of the file. 
You may use you personal keys. Ensure that this account has the permissions listed below or gain them from a group or role.
```
export AWS_ACCESS_KEY_ID=AKIAIOSYOURCCESSKEY
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfYOURSECRETKEY
export AWS_DEFAULT_REGION=us-west-2
```

When this is update the current shell. Either open a new Terminal or use the command below
````
source ~/.bashrc
````

Ensure that the user who owns this credentials has the permissions below.

Required permissions for a quick sandbox setup
- AmazonS3FullAccess
- AdministratorAccess
- AmazonSageMakerFullAccess


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


creates a domain by name salvia-labbench-<region>

creates a S3 bucket by name salvia-labbench-<region>-1<accountid>

The S3 buccket has 3 folders: sdi, data and work

A file is created at the end of the environment setup. 
It is located at the root of the environment space. The name is env_configuration.json. 
It contains information about this environment like the name of the environment. 


## destroy an environment

Once you are fone with the environment you may destroy it. 
Please keep in mind that all resources created in SageMaker Domain and on S" will be lost

For instance to destroy the LabBench environment, floow instructions below:

```
$ cd stages/labbench/terraform
$ terraform destroy 
```

For more information refer to the Terraform page https://developer.hashicorp.com/terraform/cli/commands/destroy
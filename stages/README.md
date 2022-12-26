# Salvia Stages

This section consists in environment's setups for different stages

## Environments and main features

| Name | Description | Major Features |
| ---- | ----------- | -------------- |
| [LabBench](labbench/README.md) | Quick setup for lab environments | create an S3 bucket and a SageMaker Domain |


## Blueprint

Environment setups leverage
- AWS services, especially S3, SageMaker, IAM
- Terraform


## Prerequisites

This is expected to be run from within the AWS account in Cloud9. 

It should run in another type of environment like an EC2 instance, or a local setup with AWS CLI configured.
These configuration are not tested though.

Before running one of those setups please ensure that the following pre-requisites are done.

### Setup a Cloud9 instance

Setup a Cloud9 environment in the region you want to operate the environment

Currently the region is defined by the region in which the cloud9 instance is running. Version 0.2 will allow to setup the region.

### Setup Git on the Cloud Instance

Once the Cloud9 insance is created, configure the git credentials.

TODO example

### Clone this repository onto the Cloud instance

### Upgrade Terraform on the Cloud9 instance

All the scripts leverage Terraform. It is preinstalled on Cloud9 environment. If you run a different setup you may want to install it.

As SageMaker studio features are new, the preinstalled version does not allow to get the aws sagemaker modules. You must upgrade the terraform version preinstalled in Cloud9.
```
$ terraform init -upgrade
```

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
```
source ~/.bashrc
```

Ensure that the user who owns this credentials has the permissions below.

Required permissions for a quick sandbox setup
- AmazonS3FullAccess
- AdministratorAccess
- AmazonSageMakerFullAccess


_Warning: do not add another profile by using aws configure. The credentials file is updated an automated manner by Cloud9 it is mess with your aws configure settings._


# Salvia Stage LabBench

LabBench is a quick setup for lab environments

- creates an S3 bucket dedicated to this environment
- creates a SageMaker Domain


## Blueprint and Prerequisites

Check stages documentation in the parent folder.

[Salvia Stages](../README.md)


## Blueprint of this environment

creates a domain by name salvia-labbench-YOUR_REGION

creates a S3 bucket by name salvia-labbench-YOUR_REGION-1-YOUR_ACCOUNT

The S3 buccket has 3 folders: sdi, data and work

A file is created at the end of the environment setup. 
It is located at the root of the environment space. The name is env_configuration.json. 
It contains information about this environment like the name of the environment. 


## Instructions for plan configuration

The first step consists in generating the configuration. 

You should run it once per Cloud9 instance and stage. You may have to run it again if you change the access key or secret key.

The script _terraform-configure.sh_ will collect information from the current context and yield configuration files. 

The script currently rely on with access key and secret key environment variables.  
Do not put these information in the script if you want to keep the script in version control.


From the root of the repository
```
$ cd stages/labbench
$ cd terraform
$ ./terraform-configure.sh
```

You may find the configuration files generated under the terraform subfolder. 
Files are named *.generated.* so they may be ignored by git leveraging the .gitignore configuration.
These files are not kept in version control as they might include secrets (account id, access keys).


## Instructions for plan initialisation

The second step consists in initializing the Terraform plan, expecially downloading Terraform modules required by the plan. 

You should run it once per Cloud9 instance and stage. You may have to run it again if you add new modules in your main.tf 

From the root of the repository
```
$ cd stages/labbench
$ cd terraform
$ terraform init -backend-config var-backend.generated.auto.tfvars
```

## Instructions for plan execution

The second step consists in executing the Terraform plan.
    
You will run it multiple time after each plan change.
    
From the root of the repository
```
$ cd stages/labbench
$ cd terraform
$ terraform validate
$ terraform  plan -out tfplan
$ terraform apply -auto-approve tfplan
```

## Instructions for destroying an environment

Once you are done with the environment you may destroy it. 
Please keep in mind that all resources created in SageMaker Domain and on S3 will be lost

For instance to destroy the LabBench environment, floow instructions below:


From the root of the repository
```
$ cd stages/labbench
$ cd terraform
$ terraform destroy 
```

For more information refer to the Terraform page https://developer.hashicorp.com/terraform/cli/commands/destroy
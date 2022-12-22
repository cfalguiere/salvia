# salvia
AWS tests


# Prerequisites


# Step LabBench

```
$ cd stages/labbench
$ ./terraform-configure.sh
$ cd terraform
$ terraform init -backend-config var-backend.generated.auto.tfvars
$ terraform validate
$ terraform  plan -out tfplan
$ terraform apply -auto-approve tfplan
```
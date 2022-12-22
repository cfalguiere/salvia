# Bootstrap backend and iam

#### variables loaded from backend config

variable region {
  type = string
}

#variable profile {
#  type = string
#}
#variable access_key {
#  type = string
#}
#variable secret_key {
#  type = string
#}
variable shared_credentials_file {
  type = string
}

# S3 states bucket
variable "bucket" {} # set in order to ignore warnings after init
variable key {
  type = string
}
variable encrypt {
  type = bool
}

#### Resources to be used :

variable environment {
  type = string
}

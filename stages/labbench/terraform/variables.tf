# Bootstrap backend and iam

#### variables loaded from backend config

variable region {
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

# generated variables

variable platform {
  type = string
}

variable platform_label {
  type = string
}

variable environment {
  type = string
}

variable environment_label {
  type = string
}

# your variables

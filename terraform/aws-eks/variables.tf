#AWS authentication variables
variable "aws_access_key" {
  type        = string
  description = "AWS Access Key"
}
variable "aws_secret_key" {
  type        = string
  description = "AWS Secret Key"
}

#AWS Region
variable "aws_region" {
  default     = "us-east-2"
  type        = string
  description = "AWS Region"
}

#AWS RDS-dev credentials
variable "db_name_dev" {
  type        = string
  description = "db_name_dev"
}

variable "db_username_dev" {
  type        = string
  description = "db_username_dev"
}

variable "db_password_dev" {
  type        = string
  description = "db_password_dev"
}

#AWS RDS-prod credentials
variable "db_name_prod" {
  type        = string
  description = "db_name_prod"
}

variable "db_username_prod" {
  type        = string
  description = "db_username_prod"
}

variable "db_password_prod" {
  type        = string
  description = "db_password_prod"
}
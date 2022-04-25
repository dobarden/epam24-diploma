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


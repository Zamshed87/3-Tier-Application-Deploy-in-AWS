variable "environment" {
  type    = string
  default = "dev"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}

variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a"]
}

variable "ami_id" {
  type    = string
  default = "ami-0360c520857e3138f"
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

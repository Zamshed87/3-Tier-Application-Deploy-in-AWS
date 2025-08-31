module "vpc" {
  source             = "../../modules/vpc"
  environment        = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "ec2" {
  source             = "../../modules/ec2"
  environment        = var.environment
  ami_id             = var.ami_id
  instance_type      = var.instance_type
  subnet_id          = module.vpc.public_subnet_id
  vpc_id             = module.vpc.vpc_id
}

module "ecr" {
  source      = "../../modules/ecr"
  environment = var.environment
}

module "vpc" {
  source             = "../../modules/vpc"
  environment        = var.environment
  vpc_cidr           = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "ecs" {
  source      = "../../modules/ecs"
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnets
}

module "ecr" {
  source      = "../../modules/ecr"
  environment = var.environment
}

module "rds" {
  source             = "../../modules/rds"
  environment        = var.environment
  db_name            = var.db_name
  db_username        = var.db_username
  db_password        = var.db_password
  instance_class     = var.rds_instance_class
  allocated_storage  = var.rds_allocated_storage
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.private_subnets
}

module "elasticache" {
  source      = "../../modules/elasticache"
  environment = var.environment
  vpc_id      = module.vpc.vpc_id
  subnet_ids  = module.vpc.private_subnets
}

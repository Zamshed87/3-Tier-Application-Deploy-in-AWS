# VPC outputs
output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_id" {
  value = module.vpc.public_subnet_id
}

# EC2 outputs
output "ec2_public_ip" {
  value = module.ec2.public_ip
}

output "ec2_private_key_path" {
  value = module.ec2.private_key_path
}

# ECR output
output "ecr_repository_url" {
  value = module.ecr.repository_url
}

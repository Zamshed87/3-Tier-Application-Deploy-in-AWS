output "vpc_id" { value = module.vpc.vpc_id }
output "ecs_cluster_id" { value = module.ecs.cluster_id }
output "rds_endpoint" { value = module.rds.endpoint }
output "redis_endpoint" { value = module.elasticache.endpoint }

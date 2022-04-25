output "RDS_dev_DNS_endpoint" {
  description = "RDS_dev_DNS endpoint"
  value       = aws_db_instance.diploma-rds-dev.endpoint
}

output "RDS_prod_DNS_endpoint" {
  description = "RDS_prod_DNS endpoint"
  value       = aws_db_instance.diploma-rds-prod.endpoint
}


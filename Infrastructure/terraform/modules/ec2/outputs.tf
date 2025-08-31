# Output the public IP of the EC2 instance
output "public_ip" {
  value = aws_instance.this.public_ip
}

# Output the path to the generated private key
output "private_key_path" {
  value = local_file.private_key.filename
}

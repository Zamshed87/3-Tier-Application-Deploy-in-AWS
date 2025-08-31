# Generate SSH key pair locally
resource "tls_private_key" "this" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# Create AWS key pair
resource "aws_key_pair" "this" {
  key_name   = "${var.environment}-key"
  public_key = tls_private_key.this.public_key_openssh
}

# Security Group
resource "aws_security_group" "this" {
  name        = "${var.environment}-sg"
  description = "Allow SSH"
  vpc_id      = var.vpc_id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "this" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.this.id]
  key_name                    = aws_key_pair.this.key_name
  associate_public_ip_address = true

  tags = {
    Name = "${var.environment}-ec2"
  }
}

# Save private key to local file
resource "local_file" "private_key" {
  content  = tls_private_key.this.private_key_pem
  filename = "${path.module}/ec2_key.pem"
}

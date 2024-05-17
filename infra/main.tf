provider "aws" {
  region = "us-east-1"
}

variable "aws_key_name" {
  default = "website.ppk"
}

#AWS EC2 instance
resource "aws_instance" "nebula-flask" {
  ami             = "ami-051f8a213df8bc089"  
  instance_type   = "t2.micro"
  iam_instance_profile = aws_iam_role.vivid_arts.name
  key_name             = "${var.aws_key_name}"
  security_groups      = ["${aws_security_group.nebula_securityg.name}"]

  tags = {
    Name = "Nebula-flask-instance"
  }
}

#security group for EC2 instance
resource "aws_security_group" "nebula_securityg" {
  name        = "nebula_securityg"
  description = "Security group for our Flask application"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Nebula-Security-Group"
  }
}

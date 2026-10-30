terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true

  endpoints {
    s3  = "http://127.0.0.1:4566"
    ec2 = "http://127.0.0.1:4566"
    iam = "http://127.0.0.1:4566"
  }
}

# 1. Intentional Vulnerability: Public S3 Bucket
resource "aws_s3_bucket" "vulnerable_bucket" {
  bucket = "my-unsafe-company-bucket-12345"
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket                  = aws_s3_bucket.vulnerable_bucket.id
  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# 2. Intentional Vulnerability: Open SSH Port 22 to 0.0.0.0/0
resource "aws_security_group" "unsafe_sg" {
  name        = "unsafe_sg"
  description = "Allow SSH from anywhere"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

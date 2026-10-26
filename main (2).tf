resource "aws_s3_bucket" "public" {
  bucket = "demo-public-bucket"
}

resource "aws_s3_bucket_acl" "public" {
  bucket = aws_s3_bucket.public.id
  acl    = "public-read"
}

resource "aws_security_group" "open" {
  name        = "wide-open"
  description = "bad"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "big" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "p4d.24xlarge"
  tags = {
    Name = "gpu-box"
  }
}

resource "aws_db_instance" "db" {
  identifier          = "demo-db"
  engine              = "postgres"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  username            = "admin"
  password            = "SuperSecret123!"
  publicly_accessible = true
  skip_final_snapshot = true
}

resource "aws_iam_policy" "admin" {
  name = "everything"
  policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [{ Effect = "Allow", Action = "*", Resource = "*" }]
  })
}

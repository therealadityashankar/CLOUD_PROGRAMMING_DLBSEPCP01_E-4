provider "aws" {
  region = var.aws_region
}

# S3 bucket for storing images
resource "aws_s3_bucket" "image_bucket" {
  bucket = var.bucket_name
}

# S3 bucket ownership controls
resource "aws_s3_bucket_ownership_controls" "image_bucket_ownership" {
  bucket = aws_s3_bucket.image_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# S3 bucket ACL
resource "aws_s3_bucket_acl" "image_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.image_bucket_ownership]
  bucket     = aws_s3_bucket.image_bucket.id
  acl        = "private"
}

# DynamoDB table for image metadata
resource "aws_dynamodb_table" "image_metadata" {
  name           = var.dynamodb_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "image_id"

  attribute {
    name = "image_id"
    type = "S"
  }
}

# IAM policy for Lambda to access S3 and DynamoDB
resource "aws_iam_policy" "lambda_policy" {
  name        = "image_service_lambda_policy"
  description = "Policy for Lambda to access S3 and DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
        ]
        Effect   = "Allow"
        Resource = [
          aws_s3_bucket.image_bucket.arn,
          "${aws_s3_bucket.image_bucket.arn}/*"
        ]
      },
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.image_metadata.arn
      },
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Lambda function
resource "aws_lambda_function" "image_service" {
  function_name    = var.lambda_function_name
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  role            = aws_iam_role.lambda_role.arn
  handler         = "app.lambda_handler"
  runtime         = "python3.9"
  timeout         = 30
  memory_size     = 256

  environment {
    variables = {
      BUCKET_NAME = aws_s3_bucket.image_bucket.bucket
    }
  }
}

# Create zip file for Lambda function
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../python"
  output_path = "${path.module}/lambda_function.zip"
}
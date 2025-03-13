variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "eu-central-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "image-service-bucket-20250314"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table for image metadata"
  type        = string
  default     = "image-metadata"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "image-getter"
} 
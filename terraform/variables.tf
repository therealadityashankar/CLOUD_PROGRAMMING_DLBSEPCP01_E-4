variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Name of the S3 bucket to store images"
  type        = string
  default     = "image-service-bucket-unique-name"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table for image metadata"
  type        = string
  default     = "image-metadata"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "image-service-function"
} 
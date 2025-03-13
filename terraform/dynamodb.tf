resource "aws_dynamodb_table" "image_metadata" {
  provider       = aws.eu_central_1
  name           = var.dynamodb_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "image_id"

  attribute {
    name = "image_id"
    type = "S"
  }
} 
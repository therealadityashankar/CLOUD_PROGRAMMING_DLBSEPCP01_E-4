resource "aws_s3_bucket" "image_bucket" {
  provider = aws.eu_central_1
  bucket = var.bucket_name
  force_destroy = true  # Allow terraform destroy to remove the bucket even if it contains objects
}

resource "aws_s3_bucket_ownership_controls" "image_bucket_ownership" {
  provider = aws.eu_central_1
  bucket = aws_s3_bucket.image_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "image_bucket_acl" {
  provider = aws.eu_central_1
  depends_on = [aws_s3_bucket_ownership_controls.image_bucket_ownership]
  bucket     = aws_s3_bucket.image_bucket.id
  acl        = "private"
}
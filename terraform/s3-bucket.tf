resource "aws_s3_bucket" "image_bucket" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_ownership_controls" "image_bucket_ownership" {
  bucket = aws_s3_bucket.image_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "image_bucket_acl" {
  depends_on = [aws_s3_bucket_ownership_controls.image_bucket_ownership]
  bucket     = aws_s3_bucket.image_bucket.id
  acl        = "private"
}
provider "aws" {
  region = var.aws_region
}

# Configure an additional provider for S3 to ensure it uses the correct region
provider "aws" {
  alias  = "eu_central_1"
  region = "eu-central-1"
}
# Image Service with AWS Lambda, S3, and DynamoDB

This project implements a simple service that retrieves images from AWS S3 and serves them via an API endpoint. The service is built using AWS Lambda, API Gateway, S3, and DynamoDB, and is deployed using Terraform.

## Architecture

- **AWS Lambda**: Handles the image retrieval logic
- **API Gateway**: Exposes the Lambda function as a REST API
- **S3**: Stores the images
- **DynamoDB**: Stores metadata about image access

## Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform installed
- Python 3.9+

## Setup

1. Clone this repository
2. Update the `.env` file with your AWS configuration
3. Update the `terraform/variables.tf` file with your preferred settings (especially the bucket name, which must be globally unique)

### Setting up the Python Environment

You can set up the Python virtual environment using the provided setup script:

```bash
./setup.sh
```

Or manually:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r python/requirements.txt
```

To deactivate the virtual environment when you're done:

```bash
deactivate
```

## Deployment

```bash
# Initialize Terraform
cd terraform
terraform init

# Plan the deployment
terraform plan

# Apply the deployment
terraform apply
```

## Usage

After deployment, Terraform will output the API Gateway URL. You can use this URL to access your images:

```
https://<api-gateway-id>.execute-api.<region>.amazonaws.com/<image-name>
```

For example, if you have an image named `example.jpg` in your S3 bucket, you can access it at:

```
https://<api-gateway-id>.execute-api.<region>.amazonaws.com/example.jpg
```

## Uploading Images

You can upload images to the S3 bucket using the AWS CLI:

```bash
aws s3 cp path/to/local/image.jpg s3://your-bucket-name/image.jpg
```

### Sample Images

The service includes 119 sample cat images uploaded to the S3 bucket. These can be accessed using the following URL pattern:

```
https://gw5jyewmo9.execute-api.us-east-1.amazonaws.com/cat{n}.jpg
```

where `{n}` is a number from 0 to 118. For example:
- `https://gw5jyewmo9.execute-api.us-east-1.amazonaws.com/cat0.jpg`
- `https://gw5jyewmo9.execute-api.us-east-1.amazonaws.com/cat42.jpg`
- `https://gw5jyewmo9.execute-api.us-east-1.amazonaws.com/cat118.jpg`

## Monitoring

The Lambda function logs all requests to CloudWatch Logs. Additionally, image access is tracked in the DynamoDB table, which includes:

- Image ID
- Access count
- Last accessed timestamp

## License

MIT 
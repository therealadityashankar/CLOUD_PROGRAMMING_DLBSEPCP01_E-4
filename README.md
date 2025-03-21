# Image Ranking Service with AWS Lambda, S3, and DynamoDB

<img src="/readme-stuff/image_ranker.png" alt="Project Image" width="200" height="200" />

This project implements a simple service that retrieves images from AWS Lambda, API Gateway, S3, and DynamoDB, and is deployed using Terraform.

# All routes so far!

### Image Routes
- `GET https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/{image}` - Get a specific image
  - Example: 
    - `https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/cat0.jpg`
    - `https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/cat42.jpg`
    - `https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/cat118.jpg`
  - Valid image numbers: 0-118

### Viewer Routes
- `GET https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/view` - Interactive image viewer interface
  - Example: 
    - `https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/view?index=0`
  - Query params:
    - `index`: Number between 0-118

### Ranking Routes
- `GET https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/rankings` - View all images sorted by score
  - Example: 
    - `https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/rankings`

### Voting Routes
- `POST https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/{image}/vote` - Vote on a specific image
  - Example: 
    - `https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/cat0.jpg/vote`
  - Request body:
    ```json
    {
      "vote": "upvote"  // or "downvote"
    }
    ```

## Setup

1. Clone this repository
2. Update the `.env` file with your AWS configuration
3. Update the `terraform/variables.tf` file with your preferred settings (especially the bucket name, which must be globally unique)

### Setting up the Python Environment

You can set up the Python virtual environment via the following way:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r python/requirements.txt
```

### Uploading Cat Images to S3

This project includes a `cat_photos` directory containing 119 cat images that are required for the application. Before using the application, these images need to be uploaded to your S3 bucket.

**Note:** The cat images have already been uploaded to the project's S3 bucket. These instructions are for setting up a new instance of the project with your own S3 bucket.

```bash
# Navigate to the cat_photos directory
cd cat_photos

# Upload all cat images to S3
aws s3 cp . s3://your-bucket-name/ --recursive --include "*.jpg" --acl public-read

# Alternatively, you can use the following command from the project root:
aws s3 cp cat_photos/ s3://your-bucket-name/ --recursive --include "*.jpg" --acl public-read
```

Replace `your-bucket-name` with the name of your S3 bucket defined in your Terraform variables.

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
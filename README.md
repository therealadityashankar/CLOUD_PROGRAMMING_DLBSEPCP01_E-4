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
https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/cat{n}.jpg
```

where `{n}` is a number from 0 to 118. For example:
- `https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/cat0.jpg`
- `https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/cat42.jpg`
- `https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/cat118.jpg`

### Interactive Features

The service includes several interactive features:

1. **Image Viewer**: View images with navigation controls
   ```
   https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/view?index=0
   ```
   This page allows you to:
   - Navigate between images
   - View image statistics (views, upvotes, downvotes)
   - Upvote or downvote images

2. **Image Rankings**: View all images ranked by score
   ```
   https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/rankings
   ```
   This page displays:
   - All images sorted by score (upvotes minus downvotes)
   - View counts and voting statistics
   - Links to view individual images

3. **Voting API**: Vote on images via POST request
   ```
   POST https://edd7t1w3f1.execute-api.eu-central-1.amazonaws.com/cat0.jpg/vote
   ```
   With JSON body:
   ```json
   {
     "vote": "upvote" // or "downvote"
   }
   ```

## Monitoring

The Lambda function logs all requests to CloudWatch Logs. Additionally, image access is tracked in the DynamoDB table, which includes:

- Image ID
- Access count
- Last accessed timestamp
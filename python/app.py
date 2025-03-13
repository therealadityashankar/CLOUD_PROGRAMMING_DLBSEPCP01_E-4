import json
import os
import base64
import boto3

# Initialize AWS clients
s3_client = boto3.client('s3')

# Get environment variables
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    """
    Lambda function handler to retrieve images from S3 and serve them via API Gateway
    """
    # Extract image name from path parameter
    image_name = event.get('pathParameters', {}).get('image')
    
    if not image_name:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Image name is required'})
        }
    
    # Get image from S3
    response = s3_client.get_object(
        Bucket=BUCKET_NAME,
        Key=image_name
    )
    
    # Get image content and content type
    image_content = response['Body'].read()
    content_type = response.get('ContentType', 'application/octet-stream')
    
    # Return image as base64 encoded string
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': content_type,
            'Content-Disposition': f'inline; filename="{image_name}"'
        },
        'body': base64.b64encode(image_content).decode('utf-8'),
        'isBase64Encoded': True
    } 
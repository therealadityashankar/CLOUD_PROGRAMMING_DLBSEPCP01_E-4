import json
import os
import base64
import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

def lambda_handler(event, context):
    """
    Lambda function handler to retrieve images from S3 and serve them via API Gateway
    """
    image_name = event.get('pathParameters', {}).get('image')
    
    if not image_name:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Image name is required'})
        }
    

    response = s3_client.get_object(
        Bucket=BUCKET_NAME,
        Key=image_name
    )
    
   
    image_content = response['Body'].read()
    content_type = response.get('ContentType', 'application/octet-stream')
    

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': content_type,
            'Content-Disposition': f'inline; filename="{image_name}"'
        },
        'body': base64.b64encode(image_content).decode('utf-8'),
        'isBase64Encoded': True
    } 
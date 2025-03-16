import json
import os
import boto3
import help
from handlers.image_handler import get_image_handler
from handlers.view_handler import view_image_handler
from handlers.rankings_handler import rankings_handler
from handlers.vote_handler import vote_handler

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
BUCKET_NAME = os.environ.get('BUCKET_NAME')
TABLE_NAME = 'image-metadata'

def lambda_handler(event, context):
    help.post_json_data("event data", event)

    http_method = event['requestContext']['http']['method']
    path = event['requestContext']['http']['path']

    help.post_json_data(http_method, path)
    
    if http_method == 'GET':
        if path.endswith('.jpg') or path.endswith('.jpeg') or path.endswith('.png'):
            return get_image_handler(event, context, s3_client, dynamodb, BUCKET_NAME, TABLE_NAME)
        elif path.endswith('/view'):
            return view_image_handler(event, context, s3_client, dynamodb, BUCKET_NAME, TABLE_NAME)
        elif path.endswith('/rankings'):
            return rankings_handler(event, context, s3_client, dynamodb, BUCKET_NAME, TABLE_NAME)
        else:
            return {
                'statusCode': 302,
                'headers': {
                    'Location': '/view'
                },
                'body': ''
            }
    elif http_method == 'POST':
        if path.endswith('/vote'):
            return vote_handler(event, context, s3_client, dynamodb, BUCKET_NAME, TABLE_NAME)
        else:
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Not found'})
            }
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Method not allowed'})
        } 
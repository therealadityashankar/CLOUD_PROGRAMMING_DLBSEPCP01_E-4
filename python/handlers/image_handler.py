import json
import base64

def get_image_handler(event, context, s3_client, dynamodb, bucket_name, table_name):
    """
    returns the image requested
    """
    path = event["requestContext"]['http']['path']
    image_name = path.split('/')[-1] if '/' in path else path

    if not image_name:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Image name is required'})
        }
    
    # Check if key exists in bucket
    try:
        s3_client.head_object(Bucket=bucket_name, Key=image_name)
    except s3_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return {
                'statusCode': 404,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': f'Image {image_name} not found'})
            }
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
    
    # Get the object since we know it exists
    response = s3_client.get_object(
        Bucket=bucket_name,
        Key=image_name
    )
    
    image_content = response['Body'].read()
    content_type = response.get('ContentType', 'application/octet-stream')
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': content_type,
            'Content-Disposition': f'inline; filename="{image_name}"',
            'Cache-Control': 'public, max-age=86400'
        },
        'body': base64.b64encode(image_content).decode('utf-8'),
        'isBase64Encoded': True
    } 
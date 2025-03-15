from handlers.utils import get_image_metadata

def view_image_handler(event, context, s3_client, dynamodb, bucket_name, table_name):
    # Extract image index from query parameters
    query_params = {}
    if 'queryStringParameters' in event and event['queryStringParameters']:
        query_params = event['queryStringParameters']
    elif 'rawQueryString' in event.get('requestContext', {}).get('http', {}):
        raw_query = event['requestContext']['http'].get('rawQueryString', '')
        if raw_query:
            query_params = dict(param.split('=') for param in raw_query.split('&') if '=' in param)
    
    image_index = int(query_params.get('index', 0))
    image_index = max(0, min(118, image_index))
    
    prev_index = max(0, image_index - 1)
    next_index = min(118, image_index + 1)
    
    image_name = f"cat{image_index}.jpg"
    metadata = get_image_metadata(image_name, dynamodb, table_name)
    
    views = metadata.get('views', 0)
    upvotes = metadata.get('upvotes', 0)
    downvotes = metadata.get('downvotes', 0)
    score = upvotes - downvotes
    
    # Read the template file
    with open('templates/view.html', 'r') as f:
        html = f.read()
    
    # Replace template variables
    replacements = {
        '--IMAGE_INDEX--': str(image_index),
        '--PREV_INDEX--': str(prev_index),
        '--NEXT_INDEX--': str(next_index),
        '--IMAGE_NAME--': image_name,
        '--VIEWS--': str(views),
        '--UPVOTES--': str(upvotes),
        '--DOWNVOTES--': str(downvotes),
        '--SCORE--': str(score)
    }
    
    for key, value in replacements.items():
        html = html.replace(key, value)
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': html
    } 
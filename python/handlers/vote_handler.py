import json
from handlers.utils import update_vote

def vote_handler(event, context, s3_client, dynamodb, bucket_name, table_name):
    # Extract image name from path
    path = ""
    if 'path' in event:
        path = event['path']
    elif 'requestContext' in event and 'http' in event['requestContext']:
        path = event['requestContext']['http'].get('path', '')
    
    image_name = path.split('/')[1] if len(path.split('/')) > 1 else None
    
    if not image_name:
        return {
            'statusCode': 400,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Image name is required'})
        }
    
    try:
        # Parse request body
        body = {}
        if 'body' in event:
            body = json.loads(event['body'] if event['body'] else '{}')
        
        vote_type = body.get('vote')
        
        if vote_type not in ['upvote', 'downvote']:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Vote must be either "upvote" or "downvote"'})
            }
        
        update_vote(image_name, vote_type, dynamodb, table_name)
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'success': True, 'message': f'{vote_type} recorded for {image_name}'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        } 
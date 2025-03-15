from datetime import datetime

def get_image_metadata(image_name, dynamodb, table_name):
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key={'image_id': image_name}
    )
    return response.get('Item', {})

def update_vote(image_name, vote_type, dynamodb, table_name):
    vote_field = 'upvotes' if vote_type == 'upvote' else 'downvotes'
    
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key={'image_id': image_name},
        UpdateExpression=f'SET {vote_field} = if_not_exists({vote_field}, :zero) + :inc, last_voted = :time',
        ExpressionAttributeValues={
            ':inc': 1,
            ':zero': 0,
            ':time': datetime.now().isoformat()
        },
        ReturnValues='UPDATED_NEW'
    )
    return response
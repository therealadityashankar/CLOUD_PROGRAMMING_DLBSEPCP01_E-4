from handlers.utils import get_image_metadata

def view_image_handler(event, context, s3_client, dynamodb, bucket_name, table_name):
    # Extract image index from query parameters
    query_params = {}
    if 'queryStringParameters' in event and event['queryStringParameters']:
        query_params = event['queryStringParameters']
    elif 'rawQueryString' in event.get('requestContext', {}).get('http', {}):
        # For HTTP API v2
        raw_query = event['requestContext']['http'].get('rawQueryString', '')
        if raw_query:
            query_params = dict(param.split('=') for param in raw_query.split('&') if '=' in param)
    
    image_index = int(query_params.get('index', 0))
    
    # Ensure index is within bounds (0-118)
    image_index = max(0, min(118, image_index))
    
    # Calculate previous and next indices
    prev_index = max(0, image_index - 1)
    next_index = min(118, image_index + 1)
    
    # Get image metadata
    image_name = f"cat{image_index}.jpg"
    metadata = get_image_metadata(image_name, dynamodb, table_name)
    
    # Create HTML response
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cat Image Viewer</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                text-align: center;
            }}
            img {{
                max-width: 100%;
                max-height: 500px;
                margin: 20px 0;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }}
            .navigation {{
                display: flex;
                justify-content: space-between;
                margin: 20px 0;
            }}
            .navigation a {{
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }}
            .voting {{
                margin: 20px 0;
            }}
            .voting button {{
                padding: 10px 20px;
                margin: 0 10px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            .upvote {{
                background-color: #4CAF50;
                color: white;
            }}
            .downvote {{
                background-color: #f44336;
                color: white;
            }}
            .stats {{
                margin: 20px 0;
                padding: 10px;
                background-color: #f9f9f9;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        <h1>Cat Image Viewer</h1>
        <div class="navigation">
            <a href="/view?index={prev_index}">Previous</a>
            <span>Image {image_index} of 118</span>
            <a href="/view?index={next_index}">Next</a>
        </div>
        <img src="/{image_name}" alt="Cat {image_index}">
        <div class="stats">
            <p>Views: {metadata.get('views', 0)}</p>
            <p>Upvotes: {metadata.get('upvotes', 0)}</p>
            <p>Downvotes: {metadata.get('downvotes', 0)}</p>
            <p>Score: {metadata.get('upvotes', 0) - metadata.get('downvotes', 0)}</p>
        </div>
        <div class="voting">
            <button class="upvote" onclick="vote('upvote')">Upvote</button>
            <button class="downvote" onclick="vote('downvote')">Downvote</button>
        </div>
        
        <p><a href="/rankings">View All Rankings</a></p>
        
        <script>
            function vote(voteType) {{
                fetch('/{image_name}/vote', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        vote: voteType
                    }})
                }})
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        alert('Vote recorded!');
                        location.reload();
                    }} else {{
                        alert('Error: ' + data.error);
                    }}
                }})
                .catch(error => {{
                    alert('Error: ' + error);
                }});
            }}
        </script>
    </body>
    </html>
    """
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': html
    } 
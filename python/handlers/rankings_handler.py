def rankings_handler(event, context, s3_client, dynamodb, bucket_name, table_name):
    table = dynamodb.Table(table_name)
    response = table.scan()
    items = response.get('Items', [])
    
    # Sort items by score (upvotes - downvotes)
    items.sort(key=lambda x: (x.get('upvotes', 0) - x.get('downvotes', 0)), reverse=True)
    
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cat Image Rankings</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            h1 {
                text-align: center;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }
            th, td {
                padding: 10px;
                border: 1px solid #ddd;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .thumbnail {
                width: 50px;
                height: 50px;
                object-fit: cover;
                border-radius: 4px;
            }
            .view-link {
                display: inline-block;
                padding: 5px 10px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <h1>Cat Image Rankings</h1>
        <table>
            <tr>
                <th>Rank</th>
                <th>Image</th>
                <th>Name</th>
                <th>Views</th>
                <th>Upvotes</th>
                <th>Downvotes</th>
                <th>Score</th>
                <th>Action</th>
            </tr>
    """
    
    for i, item in enumerate(items):
        image_name = item.get('image_id', '')
        views = item.get('views', 0)
        upvotes = item.get('upvotes', 0)
        downvotes = item.get('downvotes', 0)
        score = upvotes - downvotes
        
        # Extract image index for view link
        image_index = 0
        if image_name.startswith('cat') and image_name.endswith('.jpg'):
            try:
                image_index = int(image_name[3:-4])
            except ValueError:
                pass
        
        html += f"""
            <tr>
                <td>{i + 1}</td>
                <td><img src="/{image_name}" class="thumbnail" alt="{image_name}"></td>
                <td>{image_name}</td>
                <td>{views}</td>
                <td>{upvotes}</td>
                <td>{downvotes}</td>
                <td>{score}</td>
                <td><a href="/view?index={image_index}" class="view-link">View</a></td>
            </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': html
    }
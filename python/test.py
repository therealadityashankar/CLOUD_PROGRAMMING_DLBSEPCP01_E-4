from flask import Flask, render_template, request, jsonify
from app import lambda_handler
import json

app = Flask(__name__, template_folder='templates')

@app.route('/<path:path>', methods=['GET', 'POST'])
def catch_all(path):
    # Create an event object that mimics API Gateway's format
    event = {
        "requestContext": {
            "http": {
                "method": request.method,
                "path": f"/{path}"
            }
        }
    }
    
    # Add query parameters if present
    if request.args:
        event["queryStringParameters"] = dict(request.args)
        event["requestContext"]["http"]["rawQueryString"] = request.query_string.decode()

    # Add body if it's a POST request
    if request.method == 'POST':
        event["body"] = json.dumps(request.get_json())

    response = lambda_handler(event, None)
    
    return (
        response["body"],
        response["statusCode"],
        response["headers"]
    )

@app.route('/')
def index():
    return """
    <h1>Image Service Test Server</h1>
    <ul>
        <li><a href="/view?index=0">View Images</a></li>
        <li><a href="/rankings">Rankings</a></li>
        <li><a href="/cat0.jpg">Sample Image</a></li>
    </ul>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
import boto3
import json
from app import lambda_handler

def test_image():
    # Test getting an image
    event = {
        "requestContext": {
            "http": {
                "method": "GET",
                "path": "/cat0.jpg"
            }
        }
    }

    try:
        response = lambda_handler(event, None)
        print(f"Status Code: {response['statusCode']}")
        print(f"Headers: {json.dumps(response['headers'], indent=2)}")
        if response['statusCode'] == 200:
            print("Successfully retrieved image")
            print(f"Image size (base64): {len(response['body'])} bytes")
        else:
            print(f"Error: {response['body']}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    test_image()
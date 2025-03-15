import json
import http.client

def post_json_data(*args, **kwargs):
    """
    Sends a POST request with JSON data to the specified URL. - logging using this for the time being

    Returns:
        dict: Response data from the server
    """
    data = {"args": args, "kwargs": kwargs}
    json_data = json.dumps(data)

    conn = http.client.HTTPSConnection("httpdump.app")
    headers = {"Content-Type": "application/json"}
    
    conn.request("POST", "/dumps/d2274369-93c9-42c2-983b-1626799f8777", json_data, headers)
    response = conn.getresponse()
    conn.close()
    
    return {
        'status': response.status,
        'reason': response.reason
    }

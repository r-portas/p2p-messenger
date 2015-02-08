"""
    getip.py
    Gets the user's IP address
    (c) 2015 Roy Portas
"""

import requests
import json

api_link = "http://www.realip.info/api/p/realip.php"

def get_ip():
    """Gets the user's IP address"""
    req = requests.get(api_link)
    data = json.loads(req.text)
    return data.get("IP")

if __name__ == "__main__":
    print(get_ip())
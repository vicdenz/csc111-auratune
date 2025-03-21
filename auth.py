import os
import requests
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

auth_url = "https://accounts.spotify.com/api/token"
auth_options = {
    "grant_type": "client_credentials"
}

headers = {
    "Authorization": f"Basic {auth_header}",
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(auth_url, data=auth_options, headers=headers)

if response.status_code == 200:
    token = response.json().get("access_token")
    print(token)
else:
    print(response.json())

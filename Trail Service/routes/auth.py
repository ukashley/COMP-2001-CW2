import requests
from flask import request, jsonify

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def verify_user(owner_id):
    """Verify if a user exists in the Authenticator API based on owner_id."""
    try:
        # owner_id to credentials
        user_credentials = {
            1: {"email": "grace@plymouth.ac.uk", "password": "ISAD123!"},
            2: {"email": "tim@plymouth.ac.uk", "password": "COMP2001!"},
            3: {"email": "ada@plymouth.ac.uk", "password": "insecurePassword"},
        }

        credentials = user_credentials.get(owner_id)
        if not credentials:
            return None  # Invalid owner_id

        # Send POST request with credentials to the Authenticator API
        response = requests.post(AUTH_URL, json=credentials)
        if response.status_code == 200:
            return response.json()  # User authenticated successfully
        else:
            return None  # Authentication failed
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None


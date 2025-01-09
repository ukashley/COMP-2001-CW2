import requests

AUTH_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def verify_user(owner_id):
    try:
        user_credentials = {
            1: {"email": "grace@plymouth.ac.uk", "password": "ISAD123!"},
            2: {"email": "tim@plymouth.ac.uk", "password": "COMP2001!"},
            3: {"email": "ada@plymouth.ac.uk", "password": "insecurePassword"},
        }

        credentials = user_credentials.get(owner_id)
        if not credentials:
            return None, None  # Invalid owner_id

        response = requests.post(AUTH_URL, json=credentials)
        if response.status_code == 200:
            user_data = response.json()  # User authenticated successfully
            return user_data["email"], user_data["role"]  # Return email and role
        else:
            return None, None  # Authentication failed
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None, None

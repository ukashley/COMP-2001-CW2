import requests
from flask import request, jsonify
from functools import wraps

AUTH_BASE_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def verify_user(user_id):
    """Verify if a user exists in the Authenticator API."""
    try:
        response = requests.get(f"{AUTH_BASE_URL}/{user_id}")
        if response.status_code == 200:
            return response.json()  # User found
        else:
            return None  # User not found
    except Exception as e:
        print(f"Error verifying user: {e}")
        return None

import requests
from functools import wraps
from flask import request, jsonify

AUTH_BASE_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

def require_role(required_role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "Authorization header missing"}), 401

            # Decode the email and password from the header
            try:
                email, password = auth_header.split(":")
            except ValueError:
                return jsonify({"error": "Invalid Authorization header format. Use 'email:password'"}), 400

            # Verify the user
            response = requests.post(
                AUTH_BASE_URL,
                json={"email": email, "password": password}
            )

            if response.status_code != 200 or not response.json()[1]:  # Assuming the second value is the verification flag
                return jsonify({"error": "Invalid credentials"}), 403

            # You could also retrieve the user's role here and validate it
            user_data = response.json()
            if user_data.get("role") != required_role:
                return jsonify({"error": "Insufficient permissions"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator

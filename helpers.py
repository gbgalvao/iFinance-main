import jwt
import re

from flask import jsonify, redirect,request
from functools import wraps

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # Decode the token
            data = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            admin = data["admin"]
            if admin == False:
                return jsonify({'message': 'Access denied'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(admin, *args, **kwargs)
    return decorated_function

# This decorator function checks for a valid token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return redirect("/login")

        try:
            # Decode the token
            data = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            current_user = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

def brl(value):
    """Format value as BRL."""
    return f"R${value:,.2f}"

def find_special_char(input):
    # Define a regular expression pattern to match special characters
    pattern = r'[^\w]'  # Matches any character that is not a word character or whitespace

    # Search for the pattern in the input string
    match = re.search(pattern, input)

    # If a match is found, return True (contains special character), otherwise return False
    return bool(match)

def find_number(input):
    pattern = r'\d'

    match = re.search(pattern, input)

    return bool(match)
import jwt
import re

from flask import jsonify, g, request
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Access denied"}), 400

        try:
            # Decode the token
            data = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            if 'admin' in data:
                g.admin = data["admin"]
                if not g.admin:
                    return jsonify({'message': 'Access denied'}), 401
            else:
                return jsonify({'message': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(*args, **kwargs)

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
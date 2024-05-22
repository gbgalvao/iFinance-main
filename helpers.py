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


def check_name_field(input):
    # Definindo o padrão para o campo nome
    pattern = re.compile(r'^[A-Za-z\s]+$')

    match = pattern.match(input)

    return bool(match)


def validate_password(input):

    pattern = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>])[A-Za-z\d!@#$%^&*(),.?":{}|<>]{8,}$')

    match = pattern.match(input)

    return bool(match)

def validate_username(input):
    pattern = re.compile(r'^[A-Za-z\d]{1,20}$')

    match = pattern.match(input)

    return bool(match)

def validate_name_50char(input):
    # Definindo o padrão para o campo nome
    pattern = re.compile(r'^[A-Za-z\s]{1,50}$')

    match = pattern.match(input)

    return bool(match)
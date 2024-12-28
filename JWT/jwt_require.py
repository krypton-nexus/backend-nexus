import jwt
from flask import request, jsonify
from functools import wraps

# Secret key for decoding JWT
SECRET_KEY = "a3c4b8f7e9d2a10d8b4f4e5c6b7d1c2a7f9e3b6a4d8c5e7f9a3d4b6e8c7a2d1"

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Authorization token is missing."}), 401

        try:
            # Remove "Bearer" prefix if present
            token = token.split(" ")[1] if " " in token else token
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            # Attach user information to the request object
            request.user = {
                "id": decoded_token.get("student_id"),
                "email": decoded_token.get("email"),
                "role": decoded_token.get("role", "student")  # Default to 'student' if no role
            }
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token."}), 401

        return f(*args, **kwargs)

    return decorated_function

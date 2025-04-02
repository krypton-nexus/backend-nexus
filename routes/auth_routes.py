import jwt
import datetime
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from Database.connection import get_connection
from flask_bcrypt import Bcrypt 
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
auth_bp = Blueprint('auth', __name__)

SECRET_KEY = "a3c4b8f7e9d2a10d8b4f4e5c6b7d1c2a7f9e3b6a4d8c5e7f9a3d4b6e8c7a2d1"

# Initialize the serializer with the same secret key
serializer = URLSafeTimedSerializer(SECRET_KEY)
bcrypt = Bcrypt() 
@auth_bp.route('/login', methods=['POST'])
def login_student():
    """
    Endpoint to authenticate the student using email and password.
    """
    try:
        data = request.json
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required."}), 400

        email = data['email']
        password = data['password']

        connection = get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, email, password, is_verified FROM student WHERE email = %s", (email,))
            student = cursor.fetchone()

            if not student:
                return jsonify({"error": "Invalid email or password."}), 401

            if not student['is_verified']:
                return jsonify({"error": "Email is not verified."}), 400

            # Use bcrypt's check_password_hash to validate the password
            if not bcrypt.check_password_hash(student['password'], password):
                return jsonify({"error": "Invalid email or password."}), 401

            payload = {
                'student_id': student['id'],
                'email': student['email'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({"message": "Login successful.", "token": token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    """
    Endpoint to verify email using the token sent in the email.
    """
    try:
        # Decode the token to get the email
        email = serializer.loads(token, salt="email-verification-salt", max_age=3600)  # Token expires in 1 hour

        # Mark the student's email as verified
        connection = get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            # Check if the email exists
            cursor.execute("SELECT id, is_verified FROM student WHERE email = %s", (email,))
            result = cursor.fetchone()
            if not result:
                return jsonify({"error": "Invalid email or user not found."}), 404

            if result['is_verified']:
                return jsonify({"message": "Email is already verified!"}), 200

            # Update the `is_verified` field
            cursor.execute("UPDATE student SET is_verified = TRUE WHERE email = %s", (email,))
            connection.commit()

            return jsonify({"message": "Email successfully verified!"}), 200
    except SignatureExpired:
        return jsonify({"error": "The verification link has expired."}), 400
    except BadSignature:
        return jsonify({"error": "Invalid verification token."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@auth_bp.route('/admin/login', methods=['POST'])
def login_admin():
    """
    Endpoint to authenticate an admin using email and password.
    """
    try:
        data = request.json
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({"error": "Email and password are required."}), 400

        email = data['email']
        password = data['password']

        connection = get_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, email, password, role,club_id, is_active FROM admins WHERE email = %s", (email,))
            admin = cursor.fetchone()

            if not admin:
                return jsonify({"error": "Invalid email or password."}), 401

            if not admin['is_active']:
                return jsonify({"error": "Admin account is deactivated. Please contact support."}), 403

            # Validate the password using bcrypt
            if not bcrypt.check_password_hash(admin['password'], password):
                return jsonify({"error": "Invalid email or password."}), 401

            payload = {
                'admin_id': admin['id'],
                'email': admin['email'],
                'role': admin['role'],
                'club_id':admin['club_id'],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({"message": "Login successful.", "token": token, "role": admin['role']}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

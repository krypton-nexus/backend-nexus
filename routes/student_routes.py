from flask import Blueprint, request, jsonify
from models.student import insert_student, select_student_by_email, list_all_students
from service.emailservice import send_verification_email

student_bp = Blueprint('student', __name__)

@student_bp.route('/register', methods=['POST'])
def add_student():
    """
    Endpoint to add a new student and send a verification email.
    Expects JSON payload with student details.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input. JSON data expected."}), 400

        # Insert student into the database
        result = insert_student(data)
        if "error" in result:
            return jsonify(result), 400

        # Send a verification email
        send_verification_email(data['email'], data['first_name'])
        return jsonify({"message": f"Student added successfully. Verification email sent to {data['email']}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@student_bp.route('/<email>', methods=['GET'])
def get_student(email):
    """
    Endpoint to retrieve a student by email.
    """
    try:
        result = select_student_by_email(email)
        return jsonify(result), 200 if "id" in result else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@student_bp.route('/list', methods=['GET'])
def list_students():
    """
    Endpoint to retrieve a list of all students.
    """
    try:
        result = list_all_students()
        if "error" in result:
            return jsonify(result), 500
        elif "message" in result:
            return jsonify({"message": result["message"]}), 404
        else:
            return jsonify({"students": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

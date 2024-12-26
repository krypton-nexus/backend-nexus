from flask import Blueprint, request, jsonify
from models.membership import add_membership, delete_membership
from flask_jwt_extended import jwt_required
membership_bp = Blueprint('membership', __name__)

# Add membership
@membership_bp.route('/add', methods=['POST'])
@jwt_required()
def add_member():
    """
    Endpoint to add a new membership for a student to a club.
    Expects JSON payload with student_email and club_id.
    """
    try:
        data = request.json
        if not data or 'student_email' not in data or 'club_id' not in data:
            return jsonify({"error": "Invalid input. student_email and club_id are required."}), 400

        # Add the membership
        result = add_membership(data['student_email'], data['club_id'])
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Membership added successfully.", "status": result.get("message")}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete membership
@membership_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_member():
    """
    Endpoint to delete a student's membership from a club.
    Expects JSON payload with student_email and club_id.
    """
    try:
        data = request.json
        if not data or 'student_email' not in data or 'club_id' not in data:
            return jsonify({"error": "Invalid input. student_email and club_id are required."}), 400

        # Delete the membership
        result = delete_membership(data['student_email'], data['club_id'])
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Membership deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

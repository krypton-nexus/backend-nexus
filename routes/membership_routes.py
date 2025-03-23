from flask import Blueprint, request, jsonify
from models.membership import add_membership, delete_membership,list_all_membership,update_membership_status
from JWT.jwt_require import jwt_required
membership_bp = Blueprint('membership', __name__)

# Add membership

@membership_bp.route('/add', methods=['POST'])
@jwt_required
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

        return jsonify({"message": result.get("message")}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete membership
@membership_bp.route('/delete', methods=['DELETE'])
# @jwt_required
def delete_member():
    """
    Endpoint to delete a student's membership from a club.
    Expects JSON payload with student_id and club_id.
    """
    try:
        data = request.json
        if not data or 'student_id' not in data or 'club_id' not in data:
            return jsonify({"error": "Invalid input. student_email and club_id are required."}), 400

        # Delete the membership
        result = delete_membership(data['student_id'], data['club_id'])
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Membership deleted successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@membership_bp.route('/list', methods=['GET'])
@jwt_required
def list_members():
    """
    Endpoint to list all members of a club.
    Expects `club_id` as a query parameter.
    """
    try:
        club_id = request.args.get('club_id')
        if not club_id:
            return jsonify({"error": "club_id is required"}), 400

        # List all memberships for the club
        result = list_all_membership(club_id)
        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Update membership status
@membership_bp.route('/update/status', methods=['PUT'])
@jwt_required
def update_status():
    """
    Endpoint to update the status of a student's membership in a club.
    Expects JSON payload with student_email, club_id, and status.
    """
    try:
        data = request.json
        if not data or 'student_email' not in data or 'club_id' not in data or 'status' not in data:
            return jsonify({"error": "Invalid input. student_email, club_id, and status are required."}), 400

        # Update the membership status
        result = update_membership_status(data['student_email'], data['club_id'], data['status'])
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Membership status updated successfully."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


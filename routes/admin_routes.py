from flask import Blueprint, request, jsonify
from models.admin import insert_admin,select_admin_by_email, list_admins_by_club_id

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/add', methods=['POST'])
def add_admin():
    """
    Endpoint to add a new admin.
    Expects JSON payload with admin details.
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid input. JSON data expected."}), 400

        # Insert admin into the database
        result = insert_admin(data)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Admin added successfully.", "admin_id": result.get("admin_id")}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/email', methods=['GET'])
def get_admin(email):
    """
    Endpoint to retrieve an admin by their ID.
    """
    try:
        result =  select_admin_by_email(email)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/club/<club_id>', methods=['GET'])
def get_admins_by_club_id(club_id):
    """
    Endpoint to retrieve all admins for a specific club by its ID.
    """
    try:
        result = list_admins_by_club_id(club_id)
        if "error" in result:
            return jsonify(result), 500
        elif "message" in result:
            return jsonify({"message": result["message"]}), 404
        else:
            return jsonify({"admins": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

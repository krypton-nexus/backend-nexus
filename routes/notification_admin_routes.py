from flask import Blueprint, request, jsonify
from models.notification_admin import insert_notification, get_unread_notifications, get_all_notifications, get_unread_count, get_read_notifications,mark_notifications_as_read
from JWT.jwt_require import jwt_required
notification_admin_bp = Blueprint('notification_admin', __name__)

@notification_admin_bp.route('/add', methods=['POST'])
@jwt_required
def add_notification():
    """
    Endpoint to add a new notification.
    Expects JSON payload with `admin_email` and `notification` parameters.
    """
    try:
        data = request.json
        if not data or not data.get('admin_email') or not data.get('notification'):
            return jsonify({"error": "admin_email and notification are required"}), 400

        admin_email = data['admin_email']
        notification = data['notification']

        # Insert notification into the database
        result = insert_notification(admin_email, notification)
        if "error" in result:
            return jsonify(result), 400

        return jsonify({"message": "Notification added successfully.", "notification_id": result.get("notification_id")}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notification_admin_bp.route('/unread', methods=['GET'])
@jwt_required
def get_unread_admin_notifications():
    """
    Endpoint to get all unread notifications for an admin.
    Expects `admin_email` as a query parameter.
    """
    try:
        admin_email = request.args.get('admin_email')
        if not admin_email:
            return jsonify({"error": "admin_email is required"}), 400

        result = get_unread_notifications(admin_email)
        if "message" in result:
            return jsonify(result), 404
        return jsonify({"unread_notifications": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notification_admin_bp.route('/all', methods=['GET'])
@jwt_required
def get_all_admin_notifications():
    """
    Endpoint to retrieve all notifications (read and unread) for an admin.
    Expects `admin_email` as a query parameter.
    """
    try:
        admin_email = request.args.get('admin_email')
        if not admin_email:
            return jsonify({"error": "admin_email is required"}), 400

        result = get_all_notifications(admin_email)
        if "message" in result:
            return jsonify(result), 404
        return jsonify({"all_notifications": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notification_admin_bp.route('/unread/count', methods=['GET'])
@jwt_required
def get_unread_admin_notification_count():
    """
    Endpoint to get the count of unread notifications for an admin.
    Expects `admin_email` as a query parameter.
    """
    try:
        admin_email = request.args.get('admin_email')
        if not admin_email:
            return jsonify({"error": "admin_email is required"}), 400

        result = get_unread_count(admin_email)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notification_admin_bp.route('/read', methods=['GET'])
@jwt_required
def get_read_admin_notifications():
    """
    Endpoint to retrieve all read notifications for a specific admin.
    Expects `admin_email` as a query parameter.
    """
    try:
        admin_email = request.args.get('admin_email')
        if not admin_email:
            return jsonify({"error": "admin_email is required"}), 400

        result = get_read_notifications(admin_email)
        if "message" in result:
            return jsonify(result), 404
        return jsonify({"read_notifications": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@notification_admin_bp.route('/mark-as-read', methods=['PATCH'])
@jwt_required
def mark_notifications_as_read_endpoint():
    """
    Endpoint to mark notifications as read.
    Accepts JSON payload with `admin_email` (required) and optional `notification_id`.
    If `notification_id` is not provided, all unread notifications for the admin will be marked as read.
    """
    try:
        data = request.json
        if not data or not data.get('admin_email'):
            return jsonify({"error": "admin_email is required"}), 400

        admin_email = data['admin_email']
        notification_id = data.get('notification_id')  # Optional

        # Update notifications' read status
        result = mark_notifications_as_read(admin_email, notification_id)
        if "error" in result:
            return jsonify(result), 400

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

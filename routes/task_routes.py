from flask import Blueprint, request, jsonify
from JWT.jwt_require import jwt_required
from models.task import (
    create_task,
    get_task_by_id,
    get_all_tasks_for_memberid,
    get_all_tasks_by_clubid,
    update_task,
    delete_task,
    get_admin_tasks,
    create_admin_task
)

task_bp = Blueprint('task', __name__)

@task_bp.route('/', methods=['POST'])
@jwt_required
def create_task_route():
    """
    Endpoint to create a new task.
    Expected JSON format:
    {
        "title": "Task title",
        "description": "Task description",
        "assignee_id": 1,
        "club_id": "CLUB001",
        "due_date": "2023-12-31",
        "priority": "Medium",
        "status": "To Do"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        result = create_task(data)
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route('/<task_id>', methods=['GET'])
@jwt_required
def get_task(task_id):
    """
    Endpoint to retrieve a task by its ID.
    """
    try:
        result = get_task_by_id(task_id)
        if "error" in result:
            return jsonify(result), 404
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route('/member/<int:member_id>', methods=['GET'])
@jwt_required
def get_member_tasks(member_id):
    """
    Endpoint to get all tasks for a specific member.
    """
    try:
        result = get_all_tasks_for_memberid(member_id)
        if "error" in result:
            return jsonify(result), 500
        return jsonify({"tasks": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route('/club/<club_id>', methods=['GET'])
@jwt_required
def get_club_tasks(club_id):
    """
    Endpoint to get all tasks for a specific club.
    """
    try:
        result = get_all_tasks_by_clubid(club_id)
        if "error" in result:
            return jsonify(result), 500
        elif "message" in result:
            return jsonify(result), 404
        return jsonify({"tasks": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route('/<task_id>', methods=['PUT'])
@jwt_required
def update_task_route(task_id):
    """
    Endpoint to update a task.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        result = update_task(task_id, data)
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route('/<task_id>', methods=['DELETE'])
@jwt_required
def delete_task_route(task_id):
    """
    Endpoint to delete a task.
    """
    try:
        result = delete_task(task_id)
        if "error" in result:
            return jsonify(result), 404
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route('/admin', methods=['POST'])
@jwt_required
def create_admin_task_route():
    """
    Endpoint to create an admin task.
    Expected JSON:
    {
        "admin_email": "admin@example.com",
        "club_id": "CLUB001",
        "task_name": "Review Budget"
    }
    """
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ["admin_email", "club_id", "task_name"]):
            return jsonify({"error": "Missing required fields"}), 400

        result = create_admin_task(data["admin_email"], data["club_id"], data["task_name"])
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@task_bp.route('/admin', methods=['GET'])
@jwt_required
def get_admin_tasks_route():
    """
    Endpoint to get admin tasks.
    Requires query parameters: admin_email and club_id
    Example: /task/admin?admin_email=admin@school.edu&club_id=CLUB001
    """
    try:
        admin_email = request.args.get('admin_email')
        club_id = request.args.get('club_id')
        
        if not admin_email or not club_id:
            return jsonify({"error": "Both admin_email and club_id are required"}), 400

        result = get_admin_tasks(admin_email, club_id)
        if "error" in result:
            return jsonify(result), 500
            
        return jsonify({"tasks": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
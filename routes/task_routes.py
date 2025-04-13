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


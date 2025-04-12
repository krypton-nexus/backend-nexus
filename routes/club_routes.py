from flask import Blueprint, request, jsonify
from models.club import insert_club, select_club_by_id, list_all_clubs
from JWT.jwt_require import jwt_required
club_bp = Blueprint('club', __name__)

@club_bp.route('/<club_id>', methods=['GET'])
@jwt_required
def get_club(club_id):
    """
    Endpoint to retrieve a club by its ID.
    """
    try:
        result = select_club_by_id(club_id)
        if "error" in result:
            return jsonify(result), 404  # Not Found
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@club_bp.route('/list', methods=['GET'])
@jwt_required
def list_clubs():
    """
    Endpoint to retrieve a list of all clubs.
    """
    try:
        result = list_all_clubs()
        if "error" in result:
            return jsonify(result), 500
        elif "message" in result:
            return jsonify({"message": result["message"]}), 404  # Return a message if no clubs
        else:
            return jsonify({"clubs": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@club_bp.route('/', methods=['POST'])
@jwt_required
def create_club():
    """
    Endpoint to create a new club.
    Expected JSON format:
    {
        "id": "unique_club_id",
        "title": "Club Title",
        "welcome_msg": "Welcome Message",
        "welcome_short_para": "Welcome Short Paragraph",
        "about_club": "About the club",
        "our_activities": "Our activities description",
        "additional_information": "Additional info",
        "images_url": {
            "header image": "url_link",
            "footer image": "url_link"
        }
    }
    """
    try:
        data = request.get_json()  # Get the request data in JSON format
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Insert the club using the function from models.club
        result = insert_club(data)

        # If the result contains an error, return the error message
        if "error" in result:
            return jsonify(result), 400  # Bad request if error in insertion
        
        return jsonify(result), 201  # Successfully created the club

    except Exception as e:
        return jsonify({"error": str(e)}), 500

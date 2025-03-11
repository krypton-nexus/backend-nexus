from flask import Blueprint, request, jsonify
from models.event import insert_event, list_events_by_club, add_participant_to_event,delete_event_by_id,delete_participant_from_event
from flask_jwt_extended import jwt_required
from JWT.jwt_require import jwt_required
event_bp = Blueprint('event', __name__)

@event_bp.route('/get_events', methods=['GET'])
@jwt_required
def get_events_by_club():
    """
    Endpoint to retrieve all events for a specific club by club ID.
    """
    try:
        club_id = request.args.get('club_id')  # Extract the club_id from query parameters
        
        if not club_id:
            return jsonify({"error": "club_id is required"}), 400  # Missing club_id in the request
        
        result = list_events_by_club(club_id)  # Call function to get events for this club

        if "error" in result:
            return jsonify(result), 500  # Internal Server Error if something goes wrong
        elif "message" in result:
            return jsonify({"message": result["message"]}), 404  # No events found for the club
        else:
            return jsonify({"events": result}), 200  # Return events list

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@event_bp.route('/create', methods=['POST'])
@jwt_required
def create_event():
    """
    Endpoint to create a new event for a specific club.
    Expected JSON format:
    {
        "club_id": "unique_club_id",
        "event_name": "Event Name",
        "event_date": "YYYY-MM-DD",
        "event_time": "HH:MM",
        "venue": "Event Venue",
        "mode": "online/physical",
        "event_description": "Event description",
        "images": ["image_url_1", "image_url_2"]
    }
    """
    try:
        data = request.get_json()  # Get the request data in JSON format
        if not data:
            return jsonify({"error": "No data provided"}), 400  # Bad request if no data
        
        if not data.get('club_id') or not data.get('event_name') or not data.get('event_date'):
            return jsonify({"error": "club_id, event_name, and event_date are required"}), 400

        # Insert the event using the function from models.event
        result = insert_event(data)

        # If the result contains an error, return the error message
        if "error" in result:
            return jsonify(result), 400  # Bad request if error in event insertion
        
        return jsonify(result), 201  # Successfully created the event

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@event_bp.route('/add_participant', methods=['POST'])
@jwt_required
def add_event_participant():
    """
    Endpoint to add a participant to an event.
    Expected JSON format:
    {
        "club_id": "unique_club_id",
        "event_id": "unique_event_id",
        "student_email": "student_email@example.com"
    }
    """
    try:
        data = request.get_json()  # Get the request data in JSON format
        if not data:
            return jsonify({"error": "No data provided"}), 400  # Bad request if no data
        
        if not data.get('club_id') or not data.get('event_id') or not data.get('student_email'):
            return jsonify({"error": "club_id, event_id, and student_email are required"}), 400
        
        club_id = data['club_id']
        event_id = data['event_id']
        student_email = data['student_email']

        # Add the participant using the function from models.event
        result = add_participant_to_event(club_id, event_id, student_email)

        # If the result contains an error, return the error message
        if "error" in result:
            return jsonify(result), 400  # Bad request if error in participant update

        return jsonify(result), 200  # Successfully added the participant

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@event_bp.route('/delete_participant', methods=['DELETE'])
@jwt_required
def delete_participant():
    """
    Endpoint to delete a participant from an event.
    Expected JSON format:
    {
        "club_id": "unique_club_id",
        "event_id": "unique_event_id",
        "student_email": "student_email@example.com"
    }
    """
    try:
        data = request.get_json()  # Get the request data in JSON format
        if not data:
            return jsonify({"error": "No data provided"}), 400  # Bad request if no data
        
        if not data.get('club_id') or not data.get('event_id') or not data.get('student_email'):
            return jsonify({"error": "club_id, event_id, and student_email are required"}), 400
        
        club_id = data['club_id']
        event_id = data['event_id']
        student_email = data['student_email']

        # Delete the participant using the function from models.event
        result = delete_participant_from_event(club_id, event_id, student_email)  # New function for deletion

        # If the result contains an error, return the error message
        if "error" in result:
            return jsonify(result), 400  # Bad request if error in participant deletion

        return jsonify(result), 200  # Successfully deleted the participant

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@event_bp.route('/delete', methods=['DELETE'])
@jwt_required
def delete_event():
    """
    Endpoint to delete an event by club ID and event ID.
    Expected parameters:
    {
        "club_id": "unique_club_id",
        "event_id": "unique_event_id"
    }
    """
    try:
        data = request.get_json()  # Get the request data in JSON format
        if not data:
            return jsonify({"error": "No data provided"}), 400  # Bad request if no data
        
        if not data.get('club_id') or not data.get('event_id'):
            return jsonify({"error": "club_id and event_id are required"}), 400

        # Get the club_id and event_id from the request data
        club_id = data['club_id']
        event_id = data['event_id']

        # Delete the event using the function from models.event
        result = delete_event_by_id(club_id, event_id)

        # If the result contains an error, return the error message
        if "error" in result:
            return jsonify(result), 400  # Bad request if error in event deletion
        
        return jsonify(result), 200  # Successfully deleted the event

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@event_bp.route('/get_participant_count', methods=['GET'])
@jwt_required()
def get_participant_count():
    """
    Endpoint to get the participant count for an event.
    Expected JSON format:
    {
        "club_id": "unique_club_id",
        "event_id": "unique_event_id"
    }
    """
    try:
        data = request.get_json()  # Get request data in JSON format
        if not data:
            return jsonify({"error": "No data provided"}), 400  # Bad request if no data

        if not data.get('club_id') or not data.get('event_id'):
            return jsonify({"error": "club_id and event_id are required"}), 400

        club_id = data['club_id']
        event_id = data['event_id']

        # Retrieve participant count from the database
        count = get_participant_count(club_id, event_id)  # Function call to fetch count

        if isinstance(count, dict) and "error" in count:
            return jsonify(count), 400  # Return error if retrieval fails

        return jsonify({"participant_count": count}), 200  # Return participant count

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal server error
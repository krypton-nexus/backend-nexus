from flask import Blueprint, request, jsonify
from models.finance import get_transactions_by_club_id
from JWT.jwt_require import jwt_required
club_bp = Blueprint('finance', __name__)

@event_bp.route('/get_transactions', methods=['GET'])
# @jwt_required
def get_transactions_by_club():
    """
    Endpoint to retrieve all transactions for a specific club by club ID.
    """
    try:
        club_id = request.args.get('club_id')  # Extract the club_id from query parameters
        
        if not club_id:
            return jsonify({"error": "club_id is required"}), 400  # Missing club_id in the request
        
        # Call the function to get transactions for the given club_id
        result = get_transactions_by_club_id(club_id)  # This is your function to fetch transactions

        if result is None:
            return jsonify({"message": "No transactions found for the specified club ID."}), 404  # No transactions found for the club
        else:
            return jsonify({"transactions": result}), 200  # Return transactions list

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error if something goes wrong

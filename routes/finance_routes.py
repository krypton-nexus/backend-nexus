from flask import Blueprint, request, jsonify
from models.finance import get_transactions_by_club_id,insert_transaction_by_club_id,insert_category
from JWT.jwt_require import jwt_required
finance_bp = Blueprint('finance', __name__)

@finance_bp.route('/get_transactions', methods=['GET'])
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

@finance_bp.route('/insert_transaction', methods=['POST'])
# @jwt_required
def insert_transaction():
    """
    Endpoint to insert a new transaction for a specific club.
    """
    try:
        # Extract transaction details from the request body
        transaction_data = request.get_json()

        # Validate the required fields in the request data
        required_fields = ["Date", "Name", "Description", "Amount", "Transaction Type", "Category Name", "club_id"]
        for field in required_fields:
            if field not in transaction_data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Extract transaction details
        club_id = transaction_data["club_id"]
        transaction_details = {
            "Date": transaction_data["Date"],
            "Name": transaction_data["Name"],
            "Description": transaction_data["Description"],
            "Amount": transaction_data["Amount"],
            "Transaction Type": transaction_data["Transaction Type"],
            "Category Name": transaction_data["Category Name"]
        }

        # Call the function to insert the transaction into the database
        insert_result=insert_transaction_by_club_id(club_id, transaction_details)
    
        if insert_result:
            return jsonify({"message": "Transaction successfully inserted."}), 201  # Transaction successfully created
        else:

            return jsonify({"error": "Failed to insert transaction."}), 500  # Insertion failed

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error if something goes wrong

@finance_bp.route('/insert_category', methods=['POST'])
def insert_category_endpoint():
    """
    Endpoint to insert a new category into the category table.
    """
    try:
        # Extract the JSON data from the request
        data = request.get_json()

        # Validate the incoming data
        if not data or 'transaction_type' not in data or 'club_id' not in data or 'category_name' not in data:
            return jsonify({"error": "Missing required fields: 'transaction_type', 'club_id', or 'category_name'"}), 400  # Bad Request

        # Extract values from the validated data
        transaction_type = data['transaction_type']
        club_id = data['club_id']
        category_name = data['category_name']

        # Call the function to insert the category into the database
        message = insert_category(transaction_type, club_id, category_name)

        # Return the result as a JSON response
        if message:
            return jsonify({"message": "Category successfully added."}), 201
        else:

            return jsonify({"error": "Failed to add category."}), 500 

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error if something goes wrong

@finance_bp.route('/delete', methods=['DELETE'])
def delete_transaction_endpoint():
    """
    Endpoint to delete a transaction from the transaction table.
    """
    try:
        # Extract the JSON data from the request
        data = request.get_json()

        # Validate the incoming data
        if not data or 'transaction_id' not in data or 'club_id' not in data:
            return jsonify({"error": "Missing required fields: 'transaction_id' or 'club_id'"}), 400  # Bad Request

        # Extract values from the validated data
        transaction_id = data['transaction_id']
        club_id = data['club_id']

        # Call the function to delete the transaction from the database
        message = delete_transaction(transaction_id, club_id)

        # Return the result as a JSON response
        if message:
            return jsonify({"message": "Transaction successfully deleted."}), 200
        else:
            return jsonify({"error": "Transaction not found or already deleted."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Internal Server Error if something goes wrong

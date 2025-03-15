from Database.connection import get_connection

def insert_transaction(data):
    """
    Inserts a new financial transaction into the database.
    :param data: Dictionary containing transaction details.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to insert transaction data without transaction_id (auto-incremented)
            insert_query = """
            INSERT INTO transactions (club_id, transaction_type_id, category_id, short_date, 
                                      transaction_description, transaction_amount)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                data['club_id'],               # Club ID
                data['transaction_type_id'],   # Transaction Type ID (1: Income, 2: Expense)
                data.get('category_id', None), # Category ID (nullable)
                data['short_date'],            # Transaction Date
                data.get('transaction_description', None),  # Description (nullable)
                data['transaction_amount']     # Amount
            ))

            connection.commit()
            return {"message": "Transaction inserted successfully"}
        
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()

def select_transaction_by_id(transaction_id):
    """
    Retrieves a financial transaction from the database by its ID.
    :param transaction_id: ID of the transaction to retrieve.
    :return: Dictionary containing transaction details or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            # SQL query to select transaction by ID
            select_query = "SELECT * FROM transactions WHERE transaction_id = %s;"
            cursor.execute(select_query, (transaction_id,))
            result = cursor.fetchone()

            if result:
                return result
            else:
                return {"error": "Transaction not found"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()          
            
def list_transactions_by_club(club_id):
    """
    Retrieves all financial transactions for a specific club.
    :param club_id: ID of the club to filter transactions.
    :return: List of dictionaries containing transaction details or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            # SQL query to select all transactions for a specific club
            select_query = "SELECT * FROM transactions WHERE club_id = %s;"
            cursor.execute(select_query, (club_id,))
            results = cursor.fetchall()

            if results:
                return results  # Return the list of transaction dictionaries
            else:
                return {"message": "No transactions found for this club"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()
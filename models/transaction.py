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
from connection import get_connection
import json
from datetime import date

# Add a new transaction (income/expense)
def add_transaction(club_id, transaction_type_id, category_id, short_date, transaction_description, transaction_amount):
    """
    Adds a financial transaction (income or expense).
    :param club_id: ID of the club.
    :param transaction_type_id: Type of transaction (income/expense).
    :param category_id: Category of income or expense.
    :param short_date: Date of transaction.
    :param transaction_description: Description of transaction.
    :param transaction_amount: Amount involved.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO transactions (club_id, transaction_type_id, category_id, short_date, 
                                      transaction_description, transaction_amount)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (club_id, transaction_type_id, category_id, short_date, 
                                          transaction_description, transaction_amount))

            connection.commit()
            return {"message": "Transaction recorded successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

# Retrieve all transactions
def get_all_transactions():
    """
    Retrieves all financial transactions.
    :return: List of transactions.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            select_query = "SELECT * FROM transactions;"
            cursor.execute(select_query)
            transactions = cursor.fetchall()

            return transactions

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

# Retrieve transactions by date range
def get_transactions_by_date(start_date, end_date):
    """
    Retrieves transactions within a specific date range.
    :param start_date: Start date.
    :param end_date: End date.
    :return: List of transactions.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            select_query = "SELECT * FROM transactions WHERE short_date BETWEEN %s AND %s;"
            cursor.execute(select_query, (start_date, end_date))
            transactions = cursor.fetchall()

            return transactions

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

# Update a transaction
def update_transaction(transaction_id, transaction_type_id, category_id, short_date, transaction_description, transaction_amount):
    """
    Updates an existing financial transaction.
    :param transaction_id: ID of the transaction.
    :param transaction_type_id: Type of transaction.
    :param category_id: Category of transaction.
    :param short_date: Date of transaction.
    :param transaction_description: Description of transaction.
    :param transaction_amount: Amount involved.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            update_query = """
            UPDATE transactions
            SET transaction_type_id = %s, category_id = %s, short_date = %s, 
                transaction_description = %s, transaction_amount = %s
            WHERE transaction_id = %s;
            """
            cursor.execute(update_query, (transaction_type_id, category_id, short_date, 
                                          transaction_description, transaction_amount, transaction_id))

            connection.commit()

            if cursor.rowcount == 0:
                return {"error": "Transaction not found"}

            return {"message": "Transaction updated successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

# Delete a transaction
def delete_transaction(transaction_id):
    """
    Deletes a financial transaction by ID.
    :param transaction_id: ID of the transaction.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            delete_query = "DELETE FROM transactions WHERE transaction_id = %s;"
            cursor.execute(delete_query, (transaction_id,))

            connection.commit()

            if cursor.rowcount == 0:
                return {"error": "Transaction not found"}

            return {"message": "Transaction deleted successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

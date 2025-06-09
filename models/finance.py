from Database.connection import get_connection
def get_transactions_by_club_id(club_id):
    """Fetches the transaction details by club_id, joined with transaction type and category, excluding the transaction ID."""
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to join the three tables and fetch the transaction details, filtered by club_id
            query = """
            SELECT t.Date, t.Name, t.Description, t.Amount,
                   tt.type_name AS transaction_type,
                   c.category_name, c.club_id,t.ID, t.created_at, t.updated_at
            FROM transactions t
            JOIN transaction_type tt ON t.transaction_type_id = tt.transaction_type_id
            JOIN category c ON t.category_id = c.category_id
            WHERE c.club_id = %s;
            """
            cursor.execute(query, (club_id,))

            # Fetch all results
            transactions = cursor.fetchall()

            if transactions:
                transaction_details_list = []
                for transaction in transactions:
                    transaction_details = {
                        "Date": transaction[0],
                        "Name": transaction[1],
                        "Description": transaction[2],
                        "Amount": transaction[3],
                        "Transaction Type": transaction[4],
                        "Category Name": transaction[5],
                        "Club ID": transaction[6],
                        "ID":transaction[7]
                    }
                    transaction_details_list.append(transaction_details)

                return transaction_details_list
            else:
                print(f"No transactions found for club_id {club_id}.")
                return None

        except Exception as e:
            print(f"Error fetching transactions for club_id {club_id}: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

def insert_transaction_by_club_id(club_id, transaction_details):
    """Inserts a new transaction for a specific club_id."""
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to insert the new transaction for the given club_id
            query = """
            INSERT INTO transactions (Date, Name, Description, Amount, transaction_type_id, category_id, club_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, 
                    (SELECT transaction_type_id FROM transaction_type WHERE type_name = %s LIMIT 1), 
                    (SELECT category_id FROM category WHERE category_name = %s AND club_id = %s LIMIT 1), 
                    %s, NOW(), NOW());
            """
            # Extract transaction details
            date = transaction_details["Date"]
            name = transaction_details["Name"]
            description = transaction_details["Description"]
            amount = transaction_details["Amount"]
            transaction_type = transaction_details["Transaction Type"]
            category_name = transaction_details["Category Name"]

            # Execute the query with the transaction details
            cursor.execute(query, (date, name, description, amount, transaction_type, category_name, club_id, club_id))

            # Commit the transaction
            connection.commit()
            return f"Transaction successfully inserted for club_id {club_id}."

        except Exception as e:
            print(f"Error inserting transaction for club_id {club_id}: {e}")
            connection.rollback()

        finally:
            cursor.close()
            connection.close()

def insert_category(transaction_type, club_id, category_name):
    """
    Inserts a new category into the category table.
    
    Parameters:
    - transaction_type: 'Income' or 'Expense' (from the frontend)
    - club_id: ID of the club (must already exist in the clubs table)
    - category_name: Name of the category to insert
    """
    transaction_type = transaction_type.strip().lower()
    if transaction_type == 'income':
        transaction_type_id = 1
    elif transaction_type == 'expense':
        transaction_type_id = 2
    else:
        print(f"Invalid transaction type: {transaction_type}")
        return

    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO category (transaction_type_id, club_id, category_name)
            VALUES (%s, %s, %s);
            """
            cursor.execute(insert_query, (transaction_type_id, club_id, category_name))
            connection.commit()
            return "Category inserted successfully."
        except Exception as e:
            connection.rollback()
            print(f"Error inserting category: {e}")
        finally:
            cursor.close()
            connection.close()

def delete_transaction(transaction_id, club_id):
    """
    Deletes a transaction from the transaction table based on transaction_id and club_id.

    Parameters:
    - transaction_id: ID of the transaction to delete
    - club_id: ID of the club to which the transaction belongs
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            delete_query = """
            DELETE FROM transactions 
            WHERE ID = %s AND club_id = %s;
            """
            cursor.execute(delete_query, (transaction_id, club_id))
            connection.commit()
            if cursor.rowcount > 0:
                return "Transaction deleted successfully."
            else:
                return "No matching transaction found."
        except Exception as e:
            connection.rollback()
            print(f"Error deleting transaction: {e}")
        finally:
            cursor.close()
            connection.close()
def get_categories_by_club_id(club_id):
    """
    Fetches all categories for a given club_id, including the transaction type name (Income/Expense).

    Parameters:
    - club_id: ID of the club whose categories are to be retrieved

    Returns:
    - A list of dictionaries with category_name and transaction_type_name
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            SELECT c.category_name, tt.type_name
            FROM category c
            JOIN transaction_type tt ON c.transaction_type_id = tt.transaction_type_id
            WHERE c.club_id = %s
            ORDER BY tt.type_name, c.category_name;
            """
            cursor.execute(query, (club_id,))
            categories = cursor.fetchall()

            category_list = []
            for category_name, type_name in categories:
                category_list.append({
                    "Category Name": category_name,
                    "Transaction Type": type_name
                })
            return category_list

        except Exception as e:
            print(f"Error fetching categories for club_id {club_id}: {e}")
            return []

        finally:
            cursor.close()
            connection.close()

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
                   c.category_name, c.club_id, t.created_at, t.updated_at
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
                        "Club ID": transaction[6]
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
            INSERT INTO transactions (Date, Name, Description, Amount, transaction_type_id, category_id, created_at, updated_at)
            VALUES (%s, %s, %s, %s, 
                    (SELECT transaction_type_id FROM transaction_type WHERE type_name = %s), 
                    (SELECT category_id FROM category WHERE category_name = %s), 
                    NOW(), NOW());
            """
            # Extract transaction details
            date = transaction_details["Date"]
            name = transaction_details["Name"]
            description = transaction_details["Description"]
            amount = transaction_details["Amount"]
            transaction_type = transaction_details["Transaction Type"]
            category_name = transaction_details["Category Name"]

            # Execute the query with the transaction details
            cursor.execute(query, (date, name, description, amount, transaction_type, category_name))

            # Commit the transaction
            connection.commit()
            print(f"Transaction successfully inserted for club_id {club_id}.")

        except Exception as e:
            print(f"Error inserting transaction for club_id {club_id}: {e}")
            connection.rollback()

        finally:
            cursor.close()
            connection.close()

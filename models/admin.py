from Database.connection import get_connection
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()  # Initialize Bcrypt for password hashing


def hash_password(password):
    """
    Hashes a plain-text password using bcrypt.
    :param password: Plain-text password.
    :return: Hashed password as a string.
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')


def insert_admin(data):
    """
    Inserts a new admin into the database after checking for existing email.
    :param data: Dictionary containing admin details.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the email already exists
            check_email_query = "SELECT COUNT(*) FROM admins WHERE email = %s"
            cursor.execute(check_email_query, (data['email'],))
            email_exists = cursor.fetchone()[0]

            if email_exists > 0:
                return {"error": "Email is already registered."}

            # Hash the password before storing it
            hashed_password = hash_password(data['password'])

            # SQL query to insert admin data
            insert_query = """
            INSERT INTO admins (club_id, first_name, last_name, email, password, phone_number, role, is_active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                data['club_id'],       # Club ID (foreign key)
                data['first_name'],    # Admin's first name
                data['last_name'],     # Admin's last name
                data['email'],         # Admin's email
                hashed_password,       # Hashed password
                data['phone_number'],  # Admin's phone number
                data['role'],          # Admin's role
                data.get('is_active', True)  # Admin's active status (default: True)
            ))
            connection.commit()
            return {"message": "Admin inserted successfully", "admin_id": cursor.lastrowid}
        
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()

def select_admin_by_email(email):
    """
    Retrieves an admin from the database by their email.
    Excludes the password column from the returned data.
    :param email: Email of the admin to retrieve.
    :return: Dictionary containing admin details or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            # SQL query to select admin by email
            select_query = "SELECT * FROM admins WHERE email = %s;"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()
            if result:
                # Remove the password field before returning
                result.pop("password", None)
                return result
            else:
                return {"error": "Admin not found"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()


def list_admins_by_club_id(club_id):
    """
    Retrieves all admins associated with a specific club ID.
    Excludes the password column from the returned data.
    :param club_id: ID of the club to filter admins.
    :return: List of dictionaries containing admin details or an error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            # SQL query to select admins by club ID
            select_query = "SELECT * FROM admins WHERE club_id = %s;"
            cursor.execute(select_query, (club_id,))
            results = cursor.fetchall()  # Fetch all rows

            if results:
                # Remove the password field from each result
                for admin in results:
                    admin.pop("password", None)
                return results  # Return the list of admin dictionaries
            else:
                return {"message": "No admins found for the specified club ID"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()

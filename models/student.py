from connection import get_connection
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()  # Initialize Bcrypt for password hashing

def hash_password(password):
    """
    Hashes a plain-text password using bcrypt.
    :param password: Plain-text password.
    :return: Hashed password as a string.
    """
    return bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(plain_password, hashed_password):
    """
    Verifies a plain-text password against a hashed password.
    :param plain_password: Plain-text password entered by the user.
    :param hashed_password: Hashed password from the database.
    :return: Boolean value indicating whether the passwords match.
    """
    return bcrypt.check_password_hash(hashed_password, plain_password)

def insert_student(data):
    """
    Inserts a new student into the database after checking for existing email and student number.
    :param data: Dictionary containing student details.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the email already exists
            check_email_query = "SELECT COUNT(*) FROM student WHERE email = %s"
            cursor.execute(check_email_query, (data['email'],))
            email_exists = cursor.fetchone()[0]

            # Check if the student number already exists
            check_student_number_query = "SELECT COUNT(*) FROM student WHERE student_number = %s"
            cursor.execute(check_student_number_query, (data['student_number'],))
            student_number_exists = cursor.fetchone()[0]

            if email_exists > 0:
                return {"error": "Email is already registered."}
            if student_number_exists > 0:
                return {"error": "Student number is already registered."}

            # Hash the password before storing it
            hashed_password = hash_password(data['password'])

            # SQL query to insert student data
            insert_query = """
            INSERT INTO student (email, first_name, last_name, phone_number, password, faculty, department, year, course_name, student_number, dob)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                data['email'],
                data['first_name'],
                data['last_name'],
                data['phone_number'],
                hashed_password,  # Save the hashed password
                data['faculty'],
                data['department'],
                data['year'],
                data['course_name'],
                data['student_number'],
                data['dob']
            ))
            connection.commit()
            return {"message": "Student inserted successfully", "student_id": cursor.lastrowid}
        
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()

def select_student_by_email(email):
    """
    Retrieves a student from the database by email.
    :param email: Email of the student to retrieve.
    :return: Dictionary containing student details or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            # SQL query to select student by email
            select_query = "SELECT * FROM student WHERE email = %s;"
            cursor.execute(select_query, (email,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                return {"error": "Student not found"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()

def list_all_students():
    """
    Retrieves all students from the database.
    :return: List of dictionaries containing student details or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            # SQL query to select all students
            select_query = "SELECT * FROM student;"
            cursor.execute(select_query)
            results = cursor.fetchall()  # Fetch all rows

            if results:
                return results  # Return the list of student dictionaries
            else:
                return {"message": "No students found"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()

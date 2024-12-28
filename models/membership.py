from connection import get_connection

def add_membership(student_email, club_id):
    """
    Adds a new membership for a student to a club, setting the default status to 'pending' for the first time.
    :param student_email: Email of the student.
    :param club_id: Club ID to which the student wants to join.
    :return: Success or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the membership already exists for this student and club
            check_membership_query = """
            SELECT status FROM membership WHERE student_email = %s AND club_id = %s;
            """
            cursor.execute(check_membership_query, (student_email, club_id))
            membership_exists = cursor.fetchone()

            if membership_exists:
                current_status = membership_exists[0]  # status is the 3rd column
                return {"message": f"Current status: {current_status}"}
            
            # SQL query to insert the membership record with default status 'pending'
            insert_query = """
            INSERT INTO membership (student_email, club_id, status)
            VALUES (%s, %s, 'pending');
            """
            cursor.execute(insert_query, (student_email, club_id))
            connection.commit()

            return {"message": "Membership added successfully, current status is 'pending'."}
        
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()

def delete_membership(student_email, club_id):
    """
    Deletes a membership of a student from a club.
    :param student_email: Email of the student whose membership needs to be deleted.
    :param club_id: Club ID from which the student should be removed.
    :return: Success or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to delete the membership record
            delete_query = """
            DELETE FROM membership
            WHERE student_email = %s AND club_id = %s;
            """
            cursor.execute(delete_query, (student_email, club_id))
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Membership deleted successfully."}
            else:
                return {"message": "No matching membership found to delete."}
        
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()

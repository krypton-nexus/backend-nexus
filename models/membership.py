from Database.connection import get_connection
from models.admin import list_admins_by_club_id
from service.emailservice import send_admin_notification
from models.notification_admin import  insert_notification
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
            VALUES (%s, %s, 'Pending');
            """
            cursor.execute(insert_query, (student_email, club_id))
            connection.commit()
            admins = list_admins_by_club_id(club_id)
            if isinstance(admins, list):
                for admin in admins:
                    admin_email = admin.get("email")
                    send_admin_notification(admin_email, student_email, club_id)
                    notification = f"Request membership from {student_email}"
                    insert_notification(admin_email,notification)

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
def update_membership_status(student_email, club_id, status):
    """
    Updates the membership status of a student in a specific club.
    :param student_email: Email of the student whose membership status is being updated.
    :param club_id: Club ID for which the student's membership status needs to be updated.
    :param status: The new status to be set (e.g., 'Accepted', 'Rejected').
    :return: Success or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the membership exists for the given student and club
            check_membership_query = """
            SELECT status FROM membership WHERE student_email = %s AND club_id = %s;
            """
            cursor.execute(check_membership_query, (student_email, club_id))
            membership_exists = cursor.fetchone()

            if not membership_exists:
                return {"message": "No membership found for this student in the specified club."}

            # SQL query to update the membership status
            update_query = """
            UPDATE membership
            SET status = %s
            WHERE student_email = %s AND club_id = %s;
            """
            cursor.execute(update_query, (status, student_email, club_id))
            connection.commit()

            if cursor.rowcount > 0:
                return {"message": f"Membership status updated to '{status}'."}
            else:
                return {"message": "Failed to update the membership status."}
        
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()
def list_all_membership(club_id):
    """
    Lists all the members of a club, including their status and the date they were added.
    :param club_id: Club ID for which the members need to be listed.
    :return: A list of memberships with student emails, statuses, and creation dates, or an error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to fetch all memberships for the given club_id, including the created_at field
            select_query = """
            SELECT student_email, status, created_at FROM membership WHERE club_id = %s;
            """
            cursor.execute(select_query, (club_id,))
            memberships = cursor.fetchall()

            if memberships:
                # Return all the memberships for the club with the created_at field
                return {"memberships": [{"student_email": email, "status": status, "created_at": created_at} 
                                        for email, status, created_at in memberships]}
            else:
                return {"message": "No memberships found for the specified club."}
        
        except Exception as e:
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()

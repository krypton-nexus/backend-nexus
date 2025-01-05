from connection import get_connection
from datetime import datetime
def insert_notification(admin_email, notification):
    """
    Inserts a new notification for an admin.
    :param admin_email: The email of the admin who should receive the notification.
    :param notification: The notification message content.
    :return: Result message indicating success or failure.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to insert a new notification
            insert_query = """
            INSERT INTO notification_admin (admin_email, notification)
            VALUES (%s, %s);
            """
            cursor.execute(insert_query, (admin_email, notification))
            connection.commit()
            return {"message": "Notification added successfully", "notification_id": cursor.lastrowid}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

def get_read_notifications(admin_email):
    """
    Retrieves all read notifications for an admin.
    :param admin_email: The email of the admin for which to retrieve read notifications.
    :return: List of read notifications or an error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            # SQL query to select all read notifications
            select_query = """
            SELECT id, notification, created_at 
            FROM notification_admin 
            WHERE admin_email = %s AND is_read = TRUE;
            """
            cursor.execute(select_query, (admin_email,))
            results = cursor.fetchall()

            if results:
                return results  # Return the list of read notifications
            else:
                return {"message": "No read notifications."}

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

def get_unread_notifications(admin_email):
    """
    Retrieves all unread notifications for an admin.
    :param admin_email: The email of the admin for which to retrieve notifications.
    :return: List of unread notifications or an error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            # SQL query to select all unread notifications
            select_query = """
            SELECT id, notification, created_at 
            FROM notification_admin 
            WHERE admin_email = %s AND is_read = FALSE;
            """
            cursor.execute(select_query, (admin_email,))
            results = cursor.fetchall()

            if results:
                return results  # Return the list of unread notifications
            else:
                return {"message": "No unread notifications."}

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

def get_all_notifications(admin_email):
    """
    Retrieves all notifications for an admin, including read and unread.
    :param admin_email: The email of the admin for which to retrieve notifications.
    :return: List of notifications or an error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)

            # SQL query to select all notifications (read and unread)
            select_query = """
            SELECT id, notification, is_read, created_at 
            FROM notification_admin 
            WHERE admin_email = %s;
            """
            cursor.execute(select_query, (admin_email,))
            results = cursor.fetchall()

            if results:
                return results  # Return the list of all notifications
            else:
                return {"message": "No notifications found for the admin."}

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

def get_unread_count(admin_email):
    """
    Retrieves the count of unread notifications for an admin.
    :param admin_email: The email of the admin for which to retrieve unread count.
    :return: Count of unread notifications or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to count unread notifications
            count_query = """
            SELECT COUNT(*) 
            FROM notification_admin 
            WHERE admin_email = %s AND is_read = FALSE;
            """
            cursor.execute(count_query, (admin_email,))
            unread_count = cursor.fetchone()[0]
            return {"unread_count": unread_count}

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

def mark_notifications_as_read(admin_email, notification_id=None):
    """
    Updates the status of notifications to 'read' (is_read = 1) and sets the updated_at field to the current time.
    :param admin_email: The email of the admin whose notifications should be updated.
    :param notification_id: (Optional) The ID of the specific notification to mark as read.
                            If not provided, all unread notifications for the admin will be marked as read.
    :return: Result message indicating success or failure.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Get the current timestamp
            updated_at = datetime.now()

            if notification_id:
                # SQL query to update a specific notification's status and timestamp
                update_query = """
                UPDATE notification_admin
                SET is_read = TRUE, updated_at = %s
                WHERE admin_email = %s AND id = %s AND is_read = FALSE;
                """
                cursor.execute(update_query, (updated_at, admin_email, notification_id))
            else:
                # SQL query to update all unread notifications' statuses and timestamps
                update_query = """
                UPDATE notification_admin
                SET is_read = TRUE, updated_at = %s
                WHERE admin_email = %s AND is_read = FALSE;
                """
                cursor.execute(update_query, (updated_at, admin_email))

            connection.commit()

            if cursor.rowcount > 0:
                return {"message": "Notifications updated successfully", "updated_count": cursor.rowcount}
            else:
                return {"message": "No unread notifications to update."}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()
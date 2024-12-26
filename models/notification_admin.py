from connection import get_connection

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

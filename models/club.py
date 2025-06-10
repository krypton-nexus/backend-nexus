from Database.connection import get_connection
import json  # To handle JSON serialization

def insert_club(data):
    """
    Inserts a new club into the database.
    :param data: Dictionary containing club details.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if the club ID already exists
            check_club_id_query = "SELECT COUNT(*) FROM clubs WHERE id = %s"
            cursor.execute(check_club_id_query, (data['id'],))
            club_id_exists = cursor.fetchone()[0]

            if club_id_exists > 0:
                return {"error": "Club ID already exists."}

                    # Safely get the first image from the array
            first_image_url = data['images_url'][0] if data['images_url'] else None

            # Prepare the image dictionary
            image_data = {'logo': first_image_url}

            # Convert to JSON string
            images_url_json = json.dumps(image_data)

            # SQL query to insert club data
            insert_query = """
            INSERT INTO clubs (id, title, welcome_msg, welcome_short_para, about_club, our_activities, additional_information, images_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                data['id'],                # Club ID
                data['title'],             # Club Title
                data['welcome_msg'],       # Welcome Message
                data['welcome_short_para'],# Welcome Short Para
                data['about_club'],        # About Club
                data['our_activities'],    # Our Activities
                data['additional_information'], # Additional Info
                images_url_json            # Images URL as JSON string
            ))

            connection.commit()
            return {"message": "Club inserted successfully"}
        
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()

def select_club_by_id(club_id):
    """
    Retrieves a club from the database by its ID.
    :param club_id: ID of the club to retrieve.
    :return: Dictionary containing club details or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            # SQL query to select club by ID
            select_query = "SELECT * FROM clubs WHERE id = %s;"
            cursor.execute(select_query, (club_id,))
            result = cursor.fetchone()
            if result:
                # If the club exists, parse the JSON field for images_url
                result['images_url'] = json.loads(result['images_url']) if result['images_url'] else None
                return result
            else:
                return {"error": "Club not found"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()

def list_all_clubs():
    """
    Retrieves all clubs from the database.
    :return: List of dictionaries containing club details or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            # SQL query to select all clubs
            select_query = "SELECT * FROM clubs;"
            cursor.execute(select_query)
            results = cursor.fetchall()  # Fetch all rows

            if results:
                # Parse images_url JSON for all clubs
                for club in results:
                    club['images_url'] = json.loads(club['images_url']) if club['images_url'] else None
                return results  # Return the list of club dictionaries
            else:
                return {"message": "No clubs found"}
        except Exception as e:
            return {"error": str(e)}
        finally:
            cursor.close()
            connection.close()

def edit_event(event_id, data):
    """
    Edits an existing event's details in the database.
    :param event_id: ID of the event to be updated.
    :param data: Dictionary containing updated event details.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to update event details dynamically
            update_fields = []
            values = []

            # Allowed fields to update
            allowed_fields = [
                "event_name", "event_date", "event_time", "venue", 
                "mode", "event_description", "category", "ispublic"
            ]

            for field in allowed_fields:
                if field in data:
                    update_fields.append(f"{field} = %s")
                    if field == "images":
                        values.append(json.dumps(data[field]))  # Convert images to JSON
                    else:
                        values.append(data[field])

            if not update_fields:
                return {"error": "No valid fields provided for update"}

            update_query = f"""
            UPDATE event_management
            SET {", ".join(update_fields)}
            WHERE id = %s;
            """
            values.append(event_id)

            cursor.execute(update_query, tuple(values))
            connection.commit()

            return {"message": "Event updated successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

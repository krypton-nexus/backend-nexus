from Database.connection import get_connection
import json  # To handle JSON serialization
from datetime import timedelta


# Helper Function to Serialize Query Results
def serialize_results(data):
    """
    Converts query results into JSON-serializable format.
    Handles timedelta objects specifically.
    """
    for record in data:
        for key, value in record.items():
            if isinstance(value, timedelta):
                record[key] = str(value)  # Convert timedelta to string
    return data


# 1. Insert Event
def insert_event(data):
    """
    Inserts a new event into the database.
    :param data: Dictionary containing event details.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to insert event data
            insert_query = """
            INSERT INTO event_management (event_name, event_date, event_time, venue, mode, event_description, participant_count, images, club_id,category,ispublic,meeting_note,count_maybe)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                data['event_name'],               # Event Name
                data['event_date'],               # Event Date
                data['event_time'],               # Event Time
                data['venue'],                    # Venue
                data['mode'],                     # Mode (online or physical)
                data['event_description'],        # Event Description
                0,                                # Initial participant count
                json.dumps(data.get('images', {})),  # Images JSON (default to empty dict)
                data['club_id'],                 # Club ID (Foreign Key)
                data['category'],
                1,
                data['meeting_note'],
                0

            ))

            connection.commit()
            return {"message": "Event inserted successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()


# 2. List Events by Club
def list_events_by_club(club_id):
    """
    Retrieves all events for a specific club from the database.
    :param club_id: The club ID for filtering events.
    :return: List of events for the given club or error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            
            # SQL query to select events by club_id
            select_query = "SELECT * FROM event_management WHERE club_id = %s;"
            cursor.execute(select_query, (club_id,))
            results = cursor.fetchall()

            if results:
                # Serialize results to handle timedelta objects
                results = serialize_results(results)
                return results
            else:
                return {"message": "No events found for this club"}

        except Exception as e:
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()
# 3. Add Participant to Event
def add_participant_to_event(club_id, event_id, student_email):
    """
    Adds a new participant to an event.
    :param club_id: Club ID to ensure the event belongs to the club.
    :param event_id: Event ID to update.
    :param student_email: Email of the student to be added to participants.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  # Ensuring that results are returned as dictionaries

            # SQL query to get event details for the specific club and event_id
            select_query = "SELECT participants, participant_count FROM event_management WHERE club_id = %s AND id = %s;"
            cursor.execute(select_query, (club_id, event_id))
            event = cursor.fetchone()  # This should now return a dictionary

            if not event:
                return {"error": "Event not found for this club"}

            participants = json.loads(event['participants']) if event['participants'] else []

            # Check if student is already in the participants list
            if student_email in participants:
                return {"message": "Student already registered as a participant."}

            # Add student email to the participants list
            participants.append(student_email)
            participant_count = event['participant_count'] + 1  # Increment participant count

            # SQL query to update the participants and participant count
            update_query = """
            UPDATE event_management 
            SET participants = %s, participant_count = %s
            WHERE club_id = %s AND id = %s;
            """
            cursor.execute(update_query, (
                json.dumps(participants),  # Updated participants list
                participant_count,         # Updated participant count
                club_id,                   # Club ID
                event_id                   # Event ID
            ))

            connection.commit()
            return {"message": "Participant added successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()


# 4. Delete Participant from Event
def delete_participant_from_event(club_id, event_id, student_email):
    """
    Deletes a participant from an event.
    :param club_id: Club ID to ensure the event belongs to the club.
    :param event_id: Event ID to remove the participant from.
    :param student_email: Email of the student to be removed from participants.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  # Ensuring that results are returned as dictionaries

            # SQL query to get event details for the specific club and event_id
            select_query = "SELECT participants, participant_count FROM event_management WHERE club_id = %s AND id = %s;"
            cursor.execute(select_query, (club_id, event_id))
            event = cursor.fetchone()  # This should now return a dictionary

            if not event:
                return {"error": "Event not found for this club"}

            participants = json.loads(event['participants']) if event['participants'] else []

            # Check if student is in the participants list
            if student_email not in participants:
                return {"message": "Student not registered as a participant."}

            # Remove student email from the participants list
            participants.remove(student_email)
            participant_count = event['participant_count'] - 1  # Decrement participant count

            # SQL query to update the participants and participant count
            update_query = """
            UPDATE event_management 
            SET participants = %s, participant_count = %s
            WHERE club_id = %s AND id = %s;
            """
            cursor.execute(update_query, (
                json.dumps(participants),  # Updated participants list
                participant_count,         # Updated participant count
                club_id,                   # Club ID
                event_id                   # Event ID
            ))

            connection.commit()
            return {"message": "Participant removed successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

# 5. Delete Event by ID
def delete_event_by_id(club_id, event_id):
    """
    Deletes an event by club ID and event ID.
    :param club_id: Club ID to ensure the event belongs to the club.
    :param event_id: Event ID to delete.
    :return: Result message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to delete the event for the specific club and event_id
            delete_query = """
            DELETE FROM event_management WHERE club_id = %s AND id = %s;
            """
            cursor.execute(delete_query, (club_id, event_id))

            # Commit the changes
            connection.commit()

            # Check if any row was deleted
            if cursor.rowcount == 0:
                return {"error": "Event not found for this club"}

            return {"message": "Event deleted successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

# 6. Retrieve Participant Count for Event
def get_participant_count(club_id, event_id):
    """
    Retrieves the participant count for a specific event.
    :param club_id: Club ID to ensure the event belongs to the club.
    :param event_id: Event ID for which participant count is needed.
    :return: Integer representing participant count or an error message.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # SQL query to get participant count
            select_query = "SELECT participant_count FROM event_management WHERE club_id = %s AND id = %s;"
            cursor.execute(select_query, (club_id, event_id))
            result = cursor.fetchone()

            if not result:
                return {"error": "Event not found for this club"}

            return result[0]  # Returning participant count as an integer

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

            # SQL query to update event details
            update_query = """
            UPDATE event_management
            SET venue = %s, event_date = %s, event_time = %s, 
                event_description = %s, mode = %s, category = %s, 
                meeting_note = %s, images = %s
            WHERE id = %s;
            """
            cursor.execute(update_query, (
                data['venue'],                # Updated Venue
                data['event_date'],           # Updated Date
                data['event_time'],           # Updated Time
                data['event_description'],    # Updated Description
                data['mode'],                 # Updated Mode (Online/Physical)
                data['category']            # Updated Category
        
            ))

            connection.commit()
            return {"message": "Event updated successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

import json
from connection import get_connection
from flask_bcrypt import Bcrypt


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

            # Serialize the image URLs into a JSON string
            images_url_json = json.dumps(data['images_url'])

            # SQL query to insert club data
            insert_query = """
            INSERT INTO clubs (id, title, welcome_msg, welcome_short_para, about_club, our_activities, additional_information, images_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                data['id'],
                data['title'],
                data['welcome_msg'],
                data['welcome_short_para'],
                data['about_club'],
                data['our_activities'],
                data['additional_information'],
                images_url_json
            ))

            connection.commit()
            return {"message": "Club inserted successfully"}
        
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()

# Insert dummy data for club_sesa and club_gavel
clubs = [
    {
        "id": "club_sesa",
        "title": "Club SESA",
        "welcome_msg": "Welcome to Club SESA!",
        "welcome_short_para": "A place for innovation and creativity.",
        "about_club": "This club focuses on technology and sustainability.",
        "our_activities": "Workshops, seminars, and competitions.",
        "additional_information": "More details will be added soon.",
        "images_url": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"]
    },
    {
        "id": "club_gavel",
        "title": "Club Gavel",
        "welcome_msg": "Join Club Gavel!",
        "welcome_short_para": "Develop your public speaking skills.",
        "about_club": "A club dedicated to improving communication skills.",
        "our_activities": "Debates, speech contests, and networking events.",
        "additional_information": "More details will be added soon.",
        "images_url": ["https://example.com/image3.jpg", "https://example.com/image4.jpg"]
    }
]

# Execute insert function for both clubs
# for club in clubs:
#     result = insert_club(club)
#     print(result)


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
                data['club_id'],
                data['first_name'],
                data['last_name'],
                data['email'],
                hashed_password,
                data['phone_number'],
                data['role'],
                data.get('is_active', True)
            ))
            connection.commit()
            return {"message": "Admin inserted successfully", "admin_id": cursor.lastrowid}
        
        except Exception as e:
            connection.rollback()
            return {"error": str(e)}
        
        finally:
            cursor.close()
            connection.close()

# Insert admin details
admins = [
    {
        "club_id": "club_sesa",
        "first_name": "Keerththanan",
        "last_name": "Vickneswaran",
        "email": "keerththananphy@gmail.com",
        "password": "keerthan",
        "phone_number": "0741468258",
        "role": "Admin",
        "is_active": True
    },
    {
        "club_id": "club_gavel",
        "first_name": "Birunthaban",
        "last_name": "Sarventhiran",
        "email": "john.doe@example.com",
        "password": "birunthaban",
        "phone_number": "0987654321",
        "role": "Admin",
        "is_active": True
    }
]

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
            INSERT INTO event_management (event_name, event_date, event_time, venue, mode, event_description, participant_count, images, club_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_query, (
                data['event_name'],               # Event Name
                data['event_date'],               # Event Date
                data['event_time'],               # Event Time
                data['venue'],                    # Venue
                data['mode'],                     # Mode (online or physical)
                data['event_description'],        # Event Description
                data['participant_count'],        # Participant Count
                json.dumps(data.get('images', {})),  # Images JSON (default to empty dict)
                data['club_id']                   # Club ID (Foreign Key)
            ))

            connection.commit()
            return {"message": "Event inserted successfully"}

        except Exception as e:
            connection.rollback()
            return {"error": str(e)}

        finally:
            cursor.close()
            connection.close()

event_1 = {
    "event_name": "The Annual General Meeting ",
    "event_date": "2025-04-25",
    "event_time": "16:00",
    "venue": "G3 Hall, Faculty of Commerce and Management Studies, University of Kelaniya.",
    "mode": "physical",
    "event_description": "The Annual General Meeting of the University of Kelaniya Gavel Club was held on the 1st of September 2022 at the G3 Hall, Faculty of Commerce and Management Studies, University of Kelaniya. The Executive Committee for the Academic Year 2020/21 was officially elected at this occasion. The meeting was graced by the Senior Treasurer of the Club, Dr. Jehan Senevirathne. The proceedings started off with the speech of the outgoing President, Gav. Sakuni Thilakarathne, followed by the presentation of Annual Report and Financial Accounts for the Academic Year 2019/20 by the outgoing Vice President - Education, Gav. Savini Samarasinghe and the outgoing Junior Treasurer, Gav. Praveen Bhawantha respectively.",
    "participant_count": 0,
    "images": ["https://nexus-se-bucket.s3.ap-south-1.amazonaws.com/Gavel/Event/Gavelevent1.jpg"],
    "club_id": 'club_gavel' # Adjust club_id as needed
}
insert_event(event_1)
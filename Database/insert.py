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
    "event_name": "Weekly educational meetings",
    "event_date": "2025-04-15",
    "event_time": "10:00",
    "venue": "G3 Hall, Faculty of Commerce and Management Studies, University of Kelaniya.",
    "mode": "physical",
    "event_description": "Educational meetings are of high significance in the Gavel club as they nurture speakers to be better versions of themselves in public speaking. The gavel club of the University of Kelaniya has weekly educational meetings on a preferable day for gavel members. Usually, weekly educational meetings are held on Fridays from 5.00 pm to 7.00 pm. The traditional physical educational meetings have transformed into virtual meetings hosted via the Zoom platform. Each educational meeting has a theme dedicated for the meeting which is set by the Toastmaster of the Day and role players like timer, ah counter, grammarian, table topics master, table topics evaluator performs their defined tasks.",
    "participant_count": 0,
    "images": ["https://nexus-se-bucket.s3.ap-south-1.amazonaws.com/Gavel/Event/Gavelevent3.jpg"],
    "club_id": 'club_gavel' # Adjust club_id as needed
}
#insert_event(event_1)

def insert_transactions():
    transactions = [
        ('2024-04-15', 'Annual Membership Renewal', 'Received annual membership renewal fee from a long-term member', 1, 'club_sesa', 12000.00, 1),
        ('2024-06-20', 'Premium Membership Dues', 'Collected premium dues from a corporate member', 1, 'club_sesa', 15000.00, 1),
        ('2024-09-10', 'Standard Membership Payment', 'Processed standard membership fee from a new member', 1, 'club_sesa', 8000.00, 1),
        ('2025-01-05', 'Membership Fee Collection', 'Membership fee collected during the annual drive', 1, 'club_sesa', 11000.00, 1),
        ('2025-02-22', 'Exclusive Membership Contribution', 'High-value membership fee received from an exclusive member', 1, 'club_sesa', 14000.00, 1),
        ('2024-05-03', 'Merchandise Sale - T-Shirt', 'Sold club-branded T-shirt at the annual fair', 3, 'club_sesa', 7000.00, 1),
        ('2024-07-18', 'Merchandise Sale - Cap', 'Revenue generated from club cap sale at a community event', 3, 'club_sesa', 6500.00, 1),
        ('2024-10-11', 'Merchandise Sale - Hoodie', 'Online orders for club hoodies brought in strong revenue', 3, 'club_sesa', 9000.00, 1),
        ('2025-02-05', 'Merchandise Sale - Mug', 'Club mug sales contributed positively to funds', 3, 'club_sesa', 7500.00, 1),
        ('2025-03-15', 'Merchandise Sale - Backpack', 'Backpack sales at the merchandise booth boosted revenue', 3, 'club_sesa', 8000.00, 1),
        ('2024-05-20', 'Event Planning Service Fee', 'Collected fee for professional event planning services provided by the club', 5, 'club_sesa', 10000.00, 1),
        ('2024-08-25', 'Catering Service Payment', 'Payment received for catering services during a major club event', 5, 'club_sesa', 12000.00, 1),
        ('2024-11-30', 'Photography Service Income', 'Income from providing photography services for a local festival', 5, 'club_sesa', 9000.00, 1),
        ('2025-01-28', 'Consultancy Service Fee', 'Received consultancy fee from a partner organization for event support', 5, 'club_sesa', 11000.00, 1),
        ('2025-03-10', 'Technical Support Service Income', 'Revenue from IT support and technical services provided to local businesses', 5, 'club_sesa', 13000.00, 1),
        ('2024-06-30', 'Charitable Donation Received', 'Received a generous donation from a local philanthropist', 7, 'club_sesa', 15000.00, 1),
        ('2024-09-22', 'Corporate Sponsorship Donation', 'Donation contributed by a corporate sponsor supporting club initiatives', 7, 'club_sesa', 18000.00, 1),
        ('2024-12-05', 'Community Donation', 'Funds donated by local community members during a fundraising event', 7, 'club_sesa', 17000.00, 1),
        ('2025-01-18', 'Individual Donor Contribution', 'Substantial donation received from an individual benefactor', 7, 'club_sesa', 16000.00, 1),
        ('2025-02-28', 'Special Donation Event', 'Funds raised during a dedicated donation drive event', 7, 'club_sesa', 19000.00, 1),
        ('2024-07-07', 'Fundraiser Proceeds', 'Income generated from the club’s annual fundraiser event', 17, 'club_sesa', 8000.00, 1),
        ('2024-08-15', 'Raffle Ticket Sales', 'Revenue from raffle ticket sales during a community event', 17, 'club_sesa', 7500.00, 1),
        ('2024-10-02', 'Online Campaign Contribution', 'Funds received from an online crowdfunding campaign for club projects', 17, 'club_sesa', 8500.00, 1),
        ('2024-12-20', 'Workshop Revenue', 'Income from hosting a community workshop on skill development', 17, 'club_sesa', 9500.00, 1),
        ('2025-03-25', 'Grant Income', 'Additional income received through small grants and support programs', 17, 'club_sesa', 9000.00, 1)
    ]

    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''INSERT INTO transactions 
            (Date, Name, Description, category_id, club_id, Amount, transaction_type_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s);'''
    cursor.executemany(query, transactions)
    
    conn.commit()
    conn.close()
    
    print("Transactions inserted successfully.")

# Call the function to insert data
insert_transactions()
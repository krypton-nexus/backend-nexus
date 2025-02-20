from connection import get_connection

def create_student_table():
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # SQL to create the student table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS student (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                phone_number VARCHAR(15) NOT NULL,
                password VARCHAR(255) NOT NULL,
                faculty VARCHAR(50) NOT NULL,
                department VARCHAR(50) NOT NULL,
                year VARCHAR(10) NOT NULL,
                course_name VARCHAR(100) NOT NULL,
                student_number VARCHAR(20) UNIQUE NOT NULL,
                dob DATE NOT NULL,
                is_verified BOOLEAN DEFAULT FALSE,  -- Tracks email verification
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            print("Table 'student' created successfully or already exists.")
        except Exception as err:
            print(f"Error creating table: {err}")
        finally:
            cursor.close()
            connection.close()

def create_club_table():
    """
    Creates the clubs table with columns for storing club details and two images.
    The 'id' is a VARCHAR(15) field and not auto-incremented.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # SQL to create the clubs table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS clubs (
                id VARCHAR(15) PRIMARY KEY,  -- Unique identifier for the club, manually assigned
                name VARCHAR(255) NOT NULL,
                description TEXT,
                image1_url VARCHAR(255),  -- URL or path to the first image
                image2_url VARCHAR(255),  -- URL or path to the second image
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_table_query)
            print("Table 'clubs' created successfully or already exists.")
        except Exception as err:
            print(f"Error creating table: {err}")
        finally:
            cursor.close()
            connection.close()


def create_admin_table():
    """
    Creates the admins table with columns for storing admin details, roles, and club association.
    The 'club_id' column matches the 'id' column in the 'clubs' table (VARCHAR(15)).
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # SQL to create the admins table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                club_id VARCHAR(15) NOT NULL,  -- Matches the VARCHAR(15) type of clubs.id
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone_number VARCHAR(15) NOT NULL,
                role ENUM('SuperAdmin', 'ManagementAdmin', 'EventAdmin', 'FinancialAdmin', 'MarketAdmin') NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,  -- Tracks whether the admin is active
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
            );
            """
            cursor.execute(create_table_query)
            print("Table 'admins' created successfully or already exists.")
        except Exception as err:
            print(f"Error creating table: {err}")
        finally:
            cursor.close()
            connection.close()
def alter_club_table():
    """
    Alters the clubs table by removing the 'description', 'image1_url', and 'image2_url' columns,
    and adding new columns: 'title', 'welcome_msg', 'welcome_short_para', 'about_club', 'our_activities',
    'additional_information'. The 'images_url' column will store a comma-separated list of image URLs.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()

            # Check if columns exist and drop them if they do
            columns_to_drop = ['description', 'image1_url', 'image2_url']
            for column in columns_to_drop:
                cursor.execute(f"SHOW COLUMNS FROM clubs LIKE '{column}'")
                result = cursor.fetchone()
                if result:
                    cursor.execute(f"ALTER TABLE clubs DROP COLUMN {column}")
                    print(f"Column '{column}' dropped.")

            # SQL to alter the clubs table
            alter_table_query = """
            ALTER TABLE clubs
            ADD COLUMN title TEXT,  -- Add 'title' column
            ADD COLUMN welcome_msg TEXT,  -- Add 'welcome_msg' column
            ADD COLUMN welcome_short_para TEXT,  -- Add 'welcome_short_para' column
            ADD COLUMN about_club TEXT,  -- Add 'about_club' column
            ADD COLUMN our_activities TEXT,  -- Add 'our_activities' column
            ADD COLUMN additional_information TEXT,  -- Add 'additional_information' column
            ADD COLUMN images_url TEXT;  -- Add 'images_url' column to store comma-separated image URLs
            """
            cursor.execute(alter_table_query)
            print("Table 'clubs' altered successfully.")
        except Exception as err:
            print(f"Error altering table: {err}")
        finally:
            cursor.close()
            connection.close()

def create_membership_table():
    """
    Creates the membership table to manage student membership in clubs.
    Includes student_id, club_id, and a status field (initially 'Pending', can be changed to 'Approved').
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # SQL to create the membership table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS membership (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,  -- Refers to the student's ID
                club_id VARCHAR(15) NOT NULL,  -- Refers to the club's ID
                status ENUM('Pending', 'Approved') DEFAULT 'Pending',  -- Tracks membership status
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE,
                FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
            );
            """
            cursor.execute(create_table_query)
            print("Table 'membership' created successfully or already exists.")
        except Exception as err:
            print(f"Error creating table: {err}")
        finally:
            cursor.close()
            connection.close()

def create_product_table():
    """
    Creates the product table to manage products associated with clubs.
    Includes product name, price, description, image link, associated club ID, and quantity.
    """
    connection = get_connection()
    if connection:
        try:
            cursor = connection.cursor()
            # SQL to create the product table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS product (
                id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL,  -- Name of the product
                product_price DECIMAL(10,2) NOT NULL,  -- Price of the product
                product_description TEXT,  -- Description of the product
                product_image_link VARCHAR(500),  -- Image link of the product
                club_id VARCHAR(15) NOT NULL,  -- Associated club ID
                product_quantity INT NOT NULL DEFAULT 0,  -- Quantity of the product available
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (club_id) REFERENCES clubs(id) ON DELETE CASCADE
            );
            """
            cursor.execute(create_table_query)
            print("Table 'product' created successfully or already exists.")
        except Exception as err:
            print(f"Error creating table: {err}")
        finally:
            cursor.close()
            connection.close()


# Call the function to create the table
# create_club_table()
# create_admin_table()
#alter_club_table()
# create_membership_table()
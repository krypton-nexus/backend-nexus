import mysql.connector

def get_connection():
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host="database-1.c9uea0aiebch.ap-south-1.rds.amazonaws.com",
            user="admin",
            password="Nexus#2024",
            database="nexus"
        )
        print("Database connection successful")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

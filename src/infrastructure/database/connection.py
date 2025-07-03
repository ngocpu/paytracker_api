import mysql.connector
from src.config import global_settings
def get_database_connection():
    try:
        connection = mysql.connector.connect(
            host=global_settings.DB_HOST,
            port=global_settings.DB_PORT,
            user=global_settings.DB_USER,
            password=global_settings.DB_PASSWORD,
            database=global_settings.DB_NAME
        )
        if connection.is_connected():
            print("Database connection established successfully.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

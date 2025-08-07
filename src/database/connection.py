import mysql.connector
from src.core import global_settings, logger
 
def get_connection():
    try:
        connection = mysql.connector.connect(
            host = global_settings.db_host,
            user = global_settings.db_user,
            password = global_settings.db_password,
            database = global_settings.db_name,
            port = global_settings.db_port
        )
        if connection.is_connected():
            logger.info("Successfully connected to the database.")
        return connection
    except mysql.connector.Error as err:
        logger.error(f"Error: {err}")
        return None
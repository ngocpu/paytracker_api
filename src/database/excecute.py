from contextlib import contextmanager
from mysql.connector import MySQLConnection
from src.core import logger

@contextmanager
def execute_query(conn:MySQLConnection, query:str, params:tuple=None):
    """Context manager to execute a query with a connection."""
    with conn.cursor(dictionary=True) as cursor:
        try:
            cursor.execute(query, params)
            yield cursor.fetchone()
        except Exception as e:
            conn.rollback()
            logger.error(f"Query execution failed: {e}")

        
    
from fastapi import FastAPI
from src.infrastructure.database.connection import get_database_connection


app = FastAPI()

@app.get("/")

def root():
    conn = get_database_connection()
    if conn:
        conn.close()
    return {"message": "Welcome to the PayTracker API!"}
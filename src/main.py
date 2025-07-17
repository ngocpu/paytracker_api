from fastapi import FastAPI
from src.infrastructure.database.connection import get_database_connection
from src.interface.routes import api_router

app = FastAPI()
app.include_router(api_router)

@app.get("/")
def root():
    # conn = get_database_connection()
    # if conn:
        # conn.close()
    return {"message": "Welcome to the PayTracker API!"}
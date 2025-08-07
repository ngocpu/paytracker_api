from fastapi import FastAPI
from src.database import get_connection
app = FastAPI()
get_connection()
@app.get("/")
def read_root():
    connection = get_connection()
    return {"Hello": "World"}
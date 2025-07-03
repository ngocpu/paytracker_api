import os
from dotenv import load_dotenv

dotenv_file = os.getenv("DOTENV_FILE")
print(f"Loading environment variables from: {dotenv_file}")
load_dotenv(dotenv_file)

class GlobalSettings:
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: int = os.getenv("DB_PORT")
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_DIALECT: str = os.getenv("DB_DIALECT")
    GG_CLIENT: str = os.getenv("GG_CLIENT_ID")
    GG_SECRET: str = os.getenv("GG_CLIENT_SECRET")
    GG_REDIRECT_URI: str = os.getenv("GG_REDIRECT_URI")

global_settings = GlobalSettings()
import os
from dotenv import load_dotenv

# Load environment variables from .env file
dotenv_file = os.getenv("DOTENV_FILE", ".env.development")
load_dotenv(dotenv_file)

class GlobalSettings:
    def __init__(self):
        self.app_name = "PayTracker"
        self.version = "1.0.0"
        self.api_prefix = "/api/v1"
        self.debug = True
        self.db_port = 3306
        self.db_host = os.getenv("DB_HOST")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.db_dialect = os.getenv("DB_DIALECT", "mysql")
        self.jwt_secret = os.getenv("JWT_SECRET", "your_jwt_secret")
        self.jwt_expiration = int(os.getenv("JWT_EXPIRATION", 30))
        self.jwt_algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.refresh_token_expire_days = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))
        self.env = os.getenv("ENV", "development")
        self.ggo_client_id = os.getenv("GGO_CLIENT_ID")
        self.ggo_client_secret = os.getenv("GGO_CLIENT_SECRET")
        self.ggo_redirect_uri = os.getenv("GGO_REDIRECT_URI")
        self.mail_user = os.getenv("MAIL_USER")
        self.mail_pass = os.getenv("MAIL_PASS")
        self.mail_host = os.getenv("MAIL_HOST")
        self.mail_port = os.getenv("MAIL_PORT", 587)
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

global_settings = GlobalSettings()

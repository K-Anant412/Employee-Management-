import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class config:
    # 1. Direct DATABASE_URL handling (common in cloud hosts like Render & Aiven)
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Standardize mysql:// to mysql+pymysql:// for SQLAlchemy PyMySQL driver compatibility
        if database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Construct from individual environment variables with defaults
        db_user = os.getenv("DB_USER", "root")
        db_host = os.getenv("DB_HOST", "localhost")
        raw_password = os.getenv("DB_PASSWORD", "")
        db_password = quote_plus(raw_password) if raw_password else ""
        db_port = os.getenv("DB_PORT", "3306")
        db_database = os.getenv("DB_NAME", "employee_management")
        db_ssl = os.getenv("DB_SSL", "false").lower()

        ssl_query = "?ssl_mode=REQUIRED" if db_ssl == "true" else ""
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}{ssl_query}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "prod-secure-ems-secret-key-2026")

    # Mail configuration
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_DEBUG = os.getenv("FLASK_ENV") == "development"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
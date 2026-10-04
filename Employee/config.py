import os
import tempfile
from dotenv import load_dotenv
from urllib.parse import quote_plus, urlparse, parse_qs, urlencode, urlunparse

load_dotenv()

class config:
    # 1. Determine SSL configuration for PyMySQL
    db_ssl = os.getenv("DB_SSL", "false").lower() == "true"
    db_ssl_ca_env = os.getenv("DB_SSL_CA") or os.getenv("AIVEN_CA_CERT")
    
    ssl_config = None
    
    if db_ssl_ca_env:
        # If CA Certificate PEM string is provided via environment variable
        ca_file_path = os.getenv("DB_SSL_CA_PATH")
        if not ca_file_path:
            temp_ca = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".pem")
            temp_ca.write(db_ssl_ca_env)
            temp_ca.close()
            ca_file_path = temp_ca.name
        ssl_config = {"ca": ca_file_path}
    elif db_ssl:
        # Default SSL/TLS for cloud MySQL (e.g. Aiven)
        ssl_config = {}

    # 2. Direct DATABASE_URL handling
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Standardize mysql:// to mysql+pymysql:// for SQLAlchemy PyMySQL driver compatibility
        if database_url.startswith("mysql://"):
            database_url = database_url.replace("mysql://", "mysql+pymysql://", 1)
            
        # Parse URL to extract and strip invalid PyMySQL query parameters like ssl-mode or ssl_mode
        parsed_url = urlparse(database_url)
        if parsed_url.query:
            query_params = parse_qs(parsed_url.query)
            
            # Check if SSL was requested via URL query string
            has_ssl_param = any(k in query_params for k in ["ssl-mode", "ssl_mode", "ssl_ca", "ssl"])
            if has_ssl_param and ssl_config is None:
                ssl_config = {}
                
            # Strip parameters that PyMySQL.connect() rejects as top-level kwargs
            for key in ["ssl-mode", "ssl_mode", "ssl_ca"]:
                query_params.pop(key, None)
                
            # Reconstruct clean URI string
            clean_query = urlencode(query_params, doseq=True)
            database_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                clean_query,
                parsed_url.fragment
            ))
            
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Construct from individual environment variables with defaults
        db_user = os.getenv("DB_USER", "root")
        db_host = os.getenv("DB_HOST", "localhost")
        raw_password = os.getenv("DB_PASSWORD", "")
        db_password = quote_plus(raw_password) if raw_password else ""
        db_port = os.getenv("DB_PORT", "3306")
        db_database = os.getenv("DB_NAME", "employee_management")
        
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
        
    # Configure PyMySQL-compatible SSL connect_args via SQLAlchemy Engine Options
    if ssl_config is not None:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "connect_args": {
                "ssl": ssl_config
            }
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}

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
import os
import tempfile
from dotenv import load_dotenv
from urllib.parse import quote_plus, urlparse, parse_qs, urlencode, urlunparse

load_dotenv()

def _build_database_configuration():
    """
    Parses DATABASE_URL or constructs it from DB_* environment variables.
    Strips invalid PyMySQL query parameters (e.g. ssl-mode, ssl_mode) from URI
    and configures PyMySQL-compatible SSL options inside connect_args.
    """
    db_ssl = os.getenv("DB_SSL", "false").lower() == "true"
    db_ssl_ca_env = os.getenv("DB_SSL_CA") or os.getenv("AIVEN_CA_CERT")
    
    ssl_config = None
    
    if db_ssl_ca_env:
        ca_file_path = os.getenv("DB_SSL_CA_PATH")
        if not ca_file_path:
            temp_ca = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".pem")
            temp_ca.write(db_ssl_ca_env)
            temp_ca.close()
            ca_file_path = temp_ca.name
        ssl_config = {"ca": ca_file_path}
    elif db_ssl:
        ssl_config = {}

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
            ssl_param_keys = ["ssl-mode", "ssl_mode", "ssl_ca", "ssl"]
            has_ssl_param = False
            for key in ssl_param_keys:
                if key in query_params:
                    has_ssl_param = True
                    break
                    
            if has_ssl_param and ssl_config is None:
                ssl_config = {}
                
            # Strip parameters that PyMySQL.connect() rejects as top-level kwargs (case-insensitive)
            for key in list(query_params.keys()):
                if key.lower() in ["ssl-mode", "ssl_mode", "ssl_ca", "ssl-ca", "sslmode", "sslca"]:
                    query_params.pop(key, None)
                
            # Reconstruct clean URI string without unsupported query parameters
            clean_query = urlencode(query_params, doseq=True)
            database_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                clean_query,
                parsed_url.fragment
            ))
            
        db_uri = database_url
    else:
        # Construct from individual environment variables with defaults
        db_user = os.getenv("DB_USER", "root")
        db_host = os.getenv("DB_HOST", "localhost")
        raw_password = os.getenv("DB_PASSWORD", "")
        db_password = quote_plus(raw_password) if raw_password else ""
        db_port = os.getenv("DB_PORT", "3306")
        db_database = os.getenv("DB_NAME", "employee_management")
        
        db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
        
    # Apply PyMySQL-compatible SSL connect_args via SQLAlchemy Engine Options
    engine_options = {}
    if ssl_config is not None:
        engine_options = {
            "connect_args": {
                "ssl": ssl_config
            }
        }
        
    return db_uri, engine_options


_db_uri, _engine_options = _build_database_configuration()


class config:
    SQLALCHEMY_DATABASE_URI = _db_uri
    SQLALCHEMY_ENGINE_OPTIONS = _engine_options
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
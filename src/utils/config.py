from .secret_key_handler import read_secret_key
from .db_url_handler import read_db_url
from dotenv import load_dotenv
import os



load_dotenv()
_secret_key = read_secret_key(".env")
_db_url = read_db_url(".env")

class AppConfig:

    BOT_SECRET = os.getenv("BOT_TOKEN")
    _FLASK_SECRET_KEY = _secret_key
    _DATABASE_URL = _db_url
    
    APP_PORT = None
    APP_DEBUG = None
    
    BOT_WEBHOOK_URL = None
    BOT_WEBHOOK_PORT = None
    

    @classmethod
    def setup(cls, port: int, debug: bool):
        
        cls.APP_PORT = port
        cls.APP_DEBUG = debug
        
        cls.BOT_WEBHOOK_PORT = port + 50
        cls.BOT_WEBHOOK_URL = f"http://127.0.0.1:{cls.BOT_WEBHOOK_PORT}/send_dm"
        

Config = AppConfig()
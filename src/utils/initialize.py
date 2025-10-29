from src.utils.args import get_args
from src.utils.config import Config
from dotenv import load_dotenv

INITIALIZED = False

def initialize_config():
    global INITIALIZED
    if INITIALIZED:
        return

    load_dotenv()

    _args = get_args()

    Config.setup(port=_args.port, debug=_args.debug)
    
    INITIALIZED = True
    
    return Config
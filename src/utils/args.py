import argparse
import os


def get_args() -> bool:
    if os.getenv('RUNNING_IN_GUNICORN') == 'true':
        real_port_str = os.getenv('APP_REAL_PORT', '8000')
        class Args:
            port = int(real_port_str)
            debug = False
        return Args()
    
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Activates debug on flask"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Defines the flask port (default: 8000)"
    )

    args = parser.parse_args()
    
    return args
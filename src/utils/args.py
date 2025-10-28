import argparse


def get_args() -> bool:
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
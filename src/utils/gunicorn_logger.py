from gunicorn.glogging import Logger
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

class ColorLogger(Logger):
    def access(self, resp, req, environ, request_time):
        try:
            status_code = int(resp.status[:3])
        except Exception:
            status_code = 0

        if 200 <= status_code < 300:
            color = Fore.GREEN
        elif 300 <= status_code < 400:
            color = Fore.YELLOW
        else:
            color = Fore.RED

        resp_status = f"{color}{resp.status[:3]}{Style.RESET_ALL}"

        remote_addr = environ.get("REMOTE_ADDR", "-")
        
        method = environ.get("REQUEST_METHOD", "-")
        method_color = Fore.CYAN if method == "GET" else Fore.YELLOW
        method = f'{method_color}{method}{Style.RESET_ALL}'

        path = environ.get("PATH_INFO", "-")
        protocol = environ.get("SERVER_PROTOCOL", "-")

        timestamp = datetime.now().strftime("%d/%b/%Y %H:%M:%S")

        log_msg = f"{remote_addr} - [{timestamp}] \"{method} {path} {protocol}\" {resp_status} -"
        self.access_log.info(log_msg)
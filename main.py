from src.app import app
from src.bot import bot
from threading import Thread
from dotenv import load_dotenv
import subprocess
import os


debug = True
load_dotenv()

def run_flask_app():
    try:
        subprocess.run([
            "gunicorn",
            "-w", "1",
            "-b", "127.0.0.1:8000",
            "--reload",
            "main:app"
        ])

    except Exception as e:
        print(f"Error running Flask app: {e}")

def run_bot():
    try:
        bot.run(os.getenv("BOT_TOKEN"))

    except Exception as e:
        print(f"Error running Discord bot: {e}")

if __name__ == "__main__":
    match debug:
        case True:
            flask_thread = Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False, 'port': 8050})
        case False:
            flask_thread = Thread(target=run_flask_app)
    bot_thread = Thread(target=run_bot)

    flask_thread.start()
    bot_thread.start()
    
    flask_thread.join()
    bot_thread.join()
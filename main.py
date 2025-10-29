from src.utils.initialize import initialize_config
initialize_config()
from src.utils.config import Config
from src.app import app
from src.bot import bot
from threading import Thread
from dotenv import load_dotenv
import subprocess
import os



load_dotenv()

def run_gunicorn(port: int):
    env = os.environ.copy()
    env['RUNNING_IN_GUNICORN'] = 'true'
    env['APP_REAL_PORT'] = str(port)
    
    global gunicorn_process
    gunicorn_process = subprocess.Popen([
        "gunicorn",
        "-k", "gthread",
        "-w", "1",
        "-b", f"127.0.0.1:{port}",
        "--threads", "8",
        "main:app",
        "--timeout", "120",
        "--access-logfile", "-",
        "--logger-class", "src.utils.gunicorn_logger.ColorLogger",
        "--access-logformat", '%(h)s - - %(t)s "%(r)s" %(s)s'
    ], env=env)

def shutdown_gunicorn():
    try:
        if gunicorn_process and gunicorn_process.poll() is None:
            print("[Gunicorn] shutting down.")
            gunicorn_process.terminate()
    except Exception as e:
        print(f"[Gunicorn] Error shutting down: {e}")

def run_bot():
    try:
        bot.run(os.getenv("BOT_TOKEN"))

    except Exception as e:
        print(f"Error running Discord bot: {e}")

def shutdown_bot():
    try:
        bot.loop.create_task(bot.close())
        print("[Bot] Shutting down.")
    except Exception as e:
        print(f"Error shutting down Discord bot: {e}")

def run_input():
    while True:
        user_input = input()

        match user_input.lower():
            case "close_bot":
                shutdown_bot()

            case "close_gunicorn":
                shutdown_gunicorn()

            case "close_term":
                break

            case "exit":
                shutdown_bot()
                shutdown_gunicorn()
                break

if __name__ == "__main__":

    match Config.APP_DEBUG:
        case True:
            flask_thread = Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False, 'port': Config.APP_PORT})
        case False:
            flask_thread = Thread(target=run_gunicorn, args=(Config.APP_PORT,))
            
    bot_thread = Thread(target=run_bot)
    input_thread = Thread(target=run_input, daemon=True)

    flask_thread.start()
    bot_thread.start()
    input_thread.start()
    
    flask_thread.join()
    bot_thread.join()
    input_thread.join()
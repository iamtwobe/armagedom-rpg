from src.utils.args import get_args
from src.app import app
from src.bot import bot
from threading import Thread
from dotenv import load_dotenv
import subprocess
import os



load_dotenv()

def run_gunicorn(port: int):
    global gunicorn_process
    gunicorn_process = subprocess.Popen([
        "gunicorn",
        "-w", "1",
        "-b", f"127.0.0.1:{port}",
        "--reload", "main:app",
        "--access-logfile", "-",
        "--logger-class", "src.utils.gunicorn_logger.ColorLogger",
        "--access-logformat", '%(h)s - - %(t)s "%(r)s" %(s)s'
    ])

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
    _args = get_args()

    debug = _args.debug
    port = _args.port

    match debug:
        case True:
            flask_thread = Thread(target=app.run, kwargs={'debug': True, 'use_reloader': False, 'port': port})
        case False:
            flask_thread = Thread(target=run_gunicorn, args=(port,))
            
    bot_thread = Thread(target=run_bot)
    input_thread = Thread(target=run_input, daemon=True)

    flask_thread.start()
    bot_thread.start()
    input_thread.start()
    
    flask_thread.join()
    bot_thread.join()
    input_thread.join()
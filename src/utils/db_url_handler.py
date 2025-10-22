from dotenv import load_dotenv
import os


def gen_db():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    users_db_path = os.path.join(base_dir, 'app', 'users', 'users.db')
    os.makedirs(os.path.dirname(users_db_path), exist_ok=True)
    users_db_uri = 'sqlite:///{}'.format(users_db_path)
    return users_db_uri

def read_db_url(env_path):
    load_dotenv(dotenv_path=env_path)

    db_url = os.getenv("DATABASE_URL")
    if db_url:
        return db_url.strip('"').strip("'")

    database_url = gen_db()
    
    with open(env_path, "a") as f:
        f.write(f"\nDATABASE_URL={database_url}\n")

    return database_url
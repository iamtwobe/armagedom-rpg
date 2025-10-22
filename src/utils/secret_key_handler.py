from dotenv import load_dotenv
import secrets
import os



def gen_secret_key(length=32):
    return secrets.token_hex(length)

def read_secret_key(env_path):
    load_dotenv(dotenv_path=env_path)

    secret = os.getenv("SECRET_KEY")
    if secret:
        return secret

    secret = gen_secret_key()
    
    with open(env_path, "a") as f:
        f.write(f"\nSECRET_KEY={secret}\n")

    return secret
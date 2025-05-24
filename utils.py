import time, hmac, hashlib, os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY").encode()
EXPIRACION = 300


def generar_token():
    ts = int(time.time())
    token = hmac.new(SECRET_KEY, str(ts).encode(), hashlib.sha256).hexdigest()
    return ts, token


def validar_token(ts, token):
    try:
        ts = int(ts)
        if abs(time.time() - ts) > EXPIRACION:
            return False
        esperado = hmac.new(SECRET_KEY, str(ts).encode(), hashlib.sha256).hexdigest()
        return hmac.compare_digest(token, esperado)
    except:
        return False

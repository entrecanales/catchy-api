from core.config import SECRET_KEY
import jwt


def get_current_user(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')

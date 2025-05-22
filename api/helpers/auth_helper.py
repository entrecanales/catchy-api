from core.config import SECRET_KEY
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

bearer_scheme = HTTPBearer()


def validate_token(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    token = credentials.credentials
    try:
        return jwt.decode(token, SECRET_KEY, algorithms='HS256')
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


def get_current_user(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms='HS256')

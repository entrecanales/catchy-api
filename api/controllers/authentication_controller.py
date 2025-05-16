from api.model.requests.authentication_requests import RegisterRequest, LoginRequest
from api.model.exceptions.authentication_exception import AuthenticationException
from api.services.authentication_service import AuthenticationService
from core.logger import get_logger
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from core.db import get_db
import uuid


class AuthenticationController:
    def __init__(self, db: Session = Depends(get_db)):
        self.service = AuthenticationService(db)
        self.logger = get_logger('catchy')

    def register(self, request: RegisterRequest):
        """
        Registers a user, that is, adds it to the database if it doesn't exist already.
        If registration is useful an email is sent to the email address indicated

        - request: the user data
        Returns the user registered
        """
        try:
            return self.service.register(request)
        except AuthenticationException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

    def login(self, request: LoginRequest):
        """
        Logins a user, fetching it from the database and, if the password matches, returns a JWT used to authenticate

        - request: the username and password
        """
        try:
            return self.service.login(request)
        except AuthenticationException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

    def me(self, token: str):
        """
        Fetches the current user from the token

        - token: the jwt token
        """
        try:
            return self.service.me(token)
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

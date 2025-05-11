from api.model.requests.authentication_requests import RegisterRequest
from api.services.authentication_service import AuthenticationService
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from core.db import get_db
from traceback import format_exc


class AuthenticationController:
    def __init__(self, db: Session = Depends(get_db)):
        self.service = AuthenticationService(db)

    def register(self, request: RegisterRequest):
        try:
            return self.service.register(request)
        except Exception as ex:
            print(format_exc())
            raise HTTPException(status_code=500, detail=str(ex))

    def login(self):
        return self.service.login

    def me(self):
        return self.service.me

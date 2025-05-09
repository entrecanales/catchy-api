from api.model.requests.authentication_requests import RegisterRequest
from fastapi import HTTPException


class AuthenticationController:
    def __init__(self, service):
        self.service = service

    def register(self, request: RegisterRequest, db):
        try:
            return self.service.register(request, db)
        except Exception as ex:
            raise HTTPException(status_code=500, detail=str(ex))

    def login(self):
        return self.service.login

    def me(self):
        return self.service.me

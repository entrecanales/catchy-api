from api.model.requests.authentication_requests import RegisterRequest

class AuthenticationController:
    def __init__(self, service):
        self.service = service

    def register(self, request: RegisterRequest):
        return self.service.register(request)

    def login(self):
        return self.service.login

    def me(self):
        return self.service.me

class AuthenticationController:
    def __init__(self, service):
        self.service = service

    def register(self):
        return self.service.register

    def login(self):
        return self.service.login

    def me(self):
        return self.service.me

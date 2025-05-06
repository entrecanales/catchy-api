from api.model.requests.authentication_requests import RegisterRequest

class AuthenticationService:
    def register(self, request: RegisterRequest):
        #TODO: Convert request to user item & divide models over multiple files
        return request.__str__()

    def login(self):
        return "Login!"

    def me(self):
        return "Me! Me! Me!"

from api.model.requests.authentication_requests import RegisterRequest
from api.model.entities.generated_models import Users
from api.repositories.authentication_repo import AuthenticationRepository


class AuthenticationService:

    def __init__(self, db):
        self.auth_repo = AuthenticationRepository(db)

    def register(self, request: RegisterRequest):
        user = Users.from_request(request)
        self.auth_repo.new_user(user)
        return "Good!"

    def login(self):
        return "Login!"

    def me(self):
        return "Me! Me! Me!"

from api.model.requests.authentication_requests import RegisterRequest
from api.model.entities.generated_models import Users as User
from api.model.schemas.authentication_schemas import RegisteredUser
from api.repositories.authentication_repo import AuthenticationRepository
from api.helpers.email_helper import send_email


class AuthenticationService:

    def __init__(self, db):
        self.auth_repo = AuthenticationRepository(db)

    def register(self, request: RegisterRequest):
        user = User.from_request(request)
        self.auth_repo.new_user(user)
        send_email(user.email)  # send a confirmation email to the user
        return RegisteredUser.from_orm(user)

    def login(self):
        return "Login!"

    def me(self):
        return "Me! Me! Me!"

from api.model.requests.authentication_requests import RegisterRequest, LoginRequest
from api.model.entities.generated_models import Users as User
from api.model.exceptions.authentication_exception import AuthenticationException
from api.model.schemas.authentication_schemas import RegisteredUser
from api.repositories.user_repo import UserRepository
from api.helpers.email_helper import send_email
from core.config import SECRET_KEY
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import jwt


class AuthenticationService:

    def __init__(self, db):
        self.user_repo = UserRepository(db)

    def register(self, request: RegisterRequest):
        user = User.from_request(request)
        try:
            self.user_repo.new_user(user)
        except IntegrityError:
            raise AuthenticationException("User already exists in the database")
        send_email(user.email)  # send a confirmation email to the user
        return RegisteredUser.from_orm(user)

    def login(self, request: LoginRequest):
        user = self.user_repo.get_user(request.username)
        if (user is None):
            raise AuthenticationException("User doesn't exist")
        # Check the password is correct
        ph = PasswordHasher()
        try:
            ph.verify(user.password, request.password)
        except VerificationError:
            raise AuthenticationException("Wrong Password")
        payload = {
            'username': request.username,
            'login-date': datetime.now().isoformat()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    def me(self):
        return "Me! Me! Me!"

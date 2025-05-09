from api.model.requests.authentication_requests import RegisterRequest
from api.model.entities.generated_models import Users
from api.repositories.authentication_repo import AuthenticationRepository
from sqlalchemy.orm import Session


class AuthenticationService:

    #def __init__(self, db: Session):  # TODO: Inject the db directly, call this constructor from... somewhere??
        #self.db = db
        #self.auth_repo = AuthenticationRepository(db)

    def register(self, request: RegisterRequest, db: Session):
        # TODO: Convert request to user item & divide models over multiple fils
        user = Users.from_request(request)
        auth_repo = AuthenticationRepository(db)
        auth_repo.new_user(user, db)
        return "Good!"

    def login(self):
        return "Login!"

    def me(self):
        return "Me! Me! Me!"

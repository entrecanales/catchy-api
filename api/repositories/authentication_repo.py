from sqlalchemy import text
from sqlalchemy.orm import Session
from api.model.entities.generated_models import Users as User
from api.helpers import model_helper as ModelHelper
from datetime import datetime, timezone


class AuthenticationRepository:
    def __init__(self, db: Session):
        self.db = db

    def new_user(self, user: User, db) -> User | None:
        
        # TODO: initialize the empty arguments to "" in the dict (no idk why this isnt green)
        # initialize the created_at att to now, the time and date of the operation
        
        user.created_at = datetime.now(tz=timezone.utc)
        user.updated_at = datetime.now(tz=timezone.utc)
        user_dict = ModelHelper.model_to_dict(user)
        print(user_dict)
        sql = text("""
                INSERT INTO users (
                    username, password, email, display_name, birth_date,
                    gender, timezone, created_at, updated_at, location, website
                )
                VALUES (
                    :username, :password, :email, :display_name, :birth_date,
                    :gender, :timezone, :created_at, :updated_at, :location, :website
                )
            """)
        db.execute(sql, user_dict)
        db.commit()

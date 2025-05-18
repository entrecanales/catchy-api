from sqlalchemy import text
from sqlalchemy.orm import Session
from api.model.entities.generated_models import Users as User
from api.helpers import model_helper as ModelHelper
from datetime import datetime, timezone
from argon2 import PasswordHasher


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def new_user(self, user: User):
        """
        Adds a new user into the database
        """
        # initialize the created_at to now, the time and date of the operation
        user.created_at = datetime.now(tz=timezone.utc)
        user.updated_at = datetime.now(tz=timezone.utc)
        # encryption of the password before inserting into the db
        ph = PasswordHasher()
        user.password = ph.hash(user.password)
        user_dict = ModelHelper.model_to_dict(user)
        sql = text("""
            INSERT INTO users (
                username, password, email, display_name, birth_date,
                gender, timezone, created_at, updated_at, is_admin, location, website
                )
                VALUES (
                    :username, :password, :email, :display_name, :birth_date,
                    :gender, :timezone, :created_at, :updated_at, :is_admin, :location, :website
                )
            """)
        self.db.execute(sql, user_dict)
        self.db.commit()

    def get_user_with_password(self, username: str):
        """
        Gets the username, password and if it's an admin from a user given the name
        """
        sql = text("""
                SELECT username, password, is_admin
                FROM users
                WHERE username = :username
            """)
        user = self.db.execute(sql, {"username": username}).fetchone()
        return user

    def get_user_by_name(self, username: str):
        """
        Gets every user attribute except for the password given the username
        """
        sql = text("""
                SELECT username, email, display_name, birth_date,
                gender, timezone, created_at, updated_at, is_admin, location, website
                FROM users
                WHERE username = :username
            """)
        user = self.db.execute(sql, {"username": username}).fetchone()
        return user

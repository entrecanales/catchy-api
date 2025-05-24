from sqlalchemy import text
from sqlalchemy.orm import Session
from api.model.entities.generated_models import Reviews as Review, Ratings as Rating
from api.helpers import model_helper as ModelHelper
from datetime import datetime, timezone
from typing import Literal


class ReviewsRepository:
    def __init__(self, db: Session):
        self.db = db

    def new_review_with_rating(self, review: Review, rating: Rating):
        """
        Adds a new review and its rating into the database
        """
        # initialize the created_at to now, the time and date of the operation
        review.created_at = datetime.now(tz=timezone.utc)
        review.updated_at = datetime.now(tz=timezone.utc)

        rating.created_at = datetime.now(tz=timezone.utc)
        rating.updated_at = datetime.now(tz=timezone.utc)

        rating_dict = ModelHelper.model_to_dict(rating)

        rating_sql = text("""
            with added_rating as (
                INSERT INTO ratings (
                    user_fk, release_fk, score, created_at, updated_at
                    )
                    VALUES (
                        :user_fk, :release_fk, :score, :created_at, :updated_at
                    )
                RETURNING id
            )
            SELECT id FROM added_rating --Return inserted rating_id
            """)
        result = self.db.execute(rating_sql, rating_dict)
        rating.id = result.fetchone().id
        review.rating_fk = rating.id

        review_dict = ModelHelper.model_to_dict(review)

        review_sql = text("""
            with added_review as (
                INSERT INTO reviews (
                    content, rating_fk, created_at, updated_at
                    )
                    VALUES (
                        :content, :rating_fk, :created_at, :updated_at
                    )
                RETURNING id
            )
            SELECT id FROM added_review --Return inserted review_id
            """)
        result = self.db.execute(review_sql, review_dict)
        review.id = result.fetchone().id
        self.db.commit()
        return review, rating

    def get_release_reviews(self,
                            release_id: int,
                            page: int,
                            rowsPerPage: int,
                            order_by: Literal["id", "name"],
                            order_asc: bool):
        """
        Gets a number of reviews and rating from a release from the database
        """
        sql = text(f"""
            SELECT re.id, re.content, re.created_at, re.updated_at, ra.user_fk, ra.release_fk,
            ra.score
            FROM reviews re INNER JOIN ratings ra ON re.rating_fk = ra.id
            WHERE ra.release_fk = :release_id
            ORDER BY {order_by} {'ASC' if order_asc else 'DESC'}
            LIMIT :limit OFFSET :offset
            """)

        params_dict = {
            'offset': (page - 1) * rowsPerPage,
            'limit': rowsPerPage,
            'asc': 'ASC' if order_asc else "DESC",
            'release_id': release_id
        }

        result = self.db.execute(sql, params_dict)
        return result.fetchall()

    def get_user_reviews(self,
                         user: str,
                         page: int,
                         rowsPerPage: int,
                         order_by: Literal["id", "name"],
                         order_asc: bool):
        """
        Gets a number of reviews of a certain user from the database
        """
        sql = text(f"""
            SELECT re.id, re.content, re.created_at, re.updated_at, ra.user_fk, ra.release_fk,
            ra.score
            FROM reviews re INNER JOIN ratings ra ON re.rating_fk = ra.id INNER JOIN Users u ON ra.user_fk = u.id
            WHERE u.username = :user
            ORDER BY {order_by} {'ASC' if order_asc else 'DESC'}
            LIMIT :limit OFFSET :offset
            """)

        params_dict = {
            'offset': (page - 1) * rowsPerPage,
            'limit': rowsPerPage,
            'asc': 'ASC' if order_asc else "DESC",
            'user': user
        }

        result = self.db.execute(sql, params_dict)
        return result.fetchall()

    def get_review(self, review_id: int):
        """
        Gets an review from the database
        """
        sql = text("""
            SELECT re.id, re.content, re.created_at, re.updated_at, ra.user_fk, ra.release_fk,
            ra.score
            FROM reviews re INNER JOIN ratings ra ON re.rating_fk = ra.id
            WHERE re.id = :review_id
            """)

        result = self.db.execute(sql, {'review_id': review_id})
        return result.fetchone()

    def update_review(self, review_id: int, score: int, content: str):
        """
        Gets an review from the database
        """

        updated_at = datetime.now(tz=timezone.utc)

        sql = text("""
            with updated_rating as (
                UPDATE reviews re SET content = :content, updated_at = :updated_at
                FROM ratings ra
                WHERE re.rating_fk = ra.id AND re.id = :review_id
              RETURNING re.id, re.content
            )
            SELECT id, content FROM updated_rating --Return updated rating_id
            """)

        result = self.db.execute(sql, {'content': content,
                                       'review_id': review_id,
                                       'updated_at': updated_at
                                       # 'score': score
                                       })
        return result.fetchone()

    def delete_review(self, review_id: int):
        """
        Deletes a review from the database
        """
        sql = text("""
            DELETE FROM reviews
            WHERE id = :review_id
            """)
        self.db.execute(sql, {'review_id': review_id})
        self.db.commit()

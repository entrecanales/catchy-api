from core.db import get_db
from core.logger import get_logger
from fastapi import HTTPException, Depends, Response
from sqlalchemy.orm import Session
from api.services.reviews_service import ReviewsService
from api.model.requests.reviews_requests import AddReviewRequest, UpdateReviewRequest
from api.model.exceptions.business_exception import BusinessException
from api.model.exceptions.users_exception import UsersException
from api.model.exceptions.releases_exception import ReleasesException
from api.model.exceptions.reviews_exception import ReviewsException
from typing import Literal
import uuid


class ReviewsController:
    def __init__(self, db: Session = Depends(get_db)):
        self.service = ReviewsService(db)
        self.logger = get_logger('catchy')

    def add_review(self, request: AddReviewRequest):
        """
        [ADMIN ONLY] Adds a new review to the database.
        If operation is successful the review is returned

        - request: the review data
        """
        try:
            return self.service.add_review(request)
        except BusinessException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

    def get_release_reviews(self,
                            release_id: int,
                            page: int,
                            rowsPerPage: int,
                            order_by: Literal["id", "name"],
                            order_asc: bool):
        """
        Gets the reviews added to a certain release, with paging

        - **release_id**: id of the release
        - **page**: the reviews page
        - **rowsPerPage**: how many reviews there will be per page
        - **order_by**: the field the results will be ordered by.
        - **order_asc**: if the data will be sorted in ascending order
        """
        # Logic
        try:
            reviews = self.service.get_release_reviews(release_id, page, rowsPerPage, order_by, order_asc)
            if len(reviews) == 0:
                return Response(status_code=204)
            return reviews
        except ReleasesException as ex:
            raise HTTPException(status_code=404, detail=str(ex))
        except BusinessException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

    def get_user_reviews(self,
                         user: str,
                         page: int,
                         rowsPerPage: int,
                         order_by: Literal["id", "name"],
                         order_asc: bool):
        """
        Gets the reviews written by a certain user, with paging

        - **user**: the name of the user
        - **page**: the reviews page
        - **rowsPerPage**: how many reviews there will be per page
        - **order_by**: the field the results will be ordered by.
        - **order_asc**: if the data will be sorted in ascending order
        """
        try:
            reviews = self.service.get_user_reviews(user, page, rowsPerPage, order_by, order_asc)
            if len(reviews) == 0:
                return Response(status_code=204)
            return reviews
        except UsersException as ex:
            raise HTTPException(status_code=404, detail=str(ex))
        except BusinessException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

    def get_review(self, review_id: int):
        """
        Gets an review of a certain id

        - **review_id**: id of an review
        """
        # Logic
        try:
            review = self.service.get_review(review_id)
            if review is not None:
                return review
        except BusinessException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")
        raise HTTPException(status_code=404, detail="Not Found")

    def update_review(self, review_id: int, request: UpdateReviewRequest):
        """
        Changes the score or content of a review

        - **review_id**: id of an review
        - **request**: the new score and/or content of the review
        """
        # Logic
        try:
            return self.service.update_review(review_id, request)
        except ReviewsException as ex:
            raise HTTPException(status_code=404, detail=str(ex))
        except BusinessException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")
        raise HTTPException(status_code=404, detail="Not Found")

    def delete_review(self, review_id: int):
        """
        Deletes a review from the database

        - **review_id**: id of an review
        """
        # Logic
        try:
            self.service.delete_review(review_id)
        except BusinessException as ex:
            raise HTTPException(status_code=404, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

from api.model.requests.reviews_requests import AddReviewRequest, UpdateReviewRequest
from api.model.entities.generated_models import Reviews as Review, Ratings as Rating
from api.model.schemas.ratings_schemas import CompleteRating
from api.model.schemas.reviews_schemas import CompleteReview
from api.model.exceptions.users_exception import UsersException
from api.model.exceptions.releases_exception import ReleasesException
from api.model.exceptions.reviews_exception import ReviewsException
from api.repositories.releases_repo import ReleasesRepository
from api.repositories.reviews_repo import ReviewsRepository
from api.repositories.users_repo import UsersRepository
from sqlalchemy.exc import IntegrityError


class ReviewsService:
    def __init__(self, db):
        self.reviews_repo = ReviewsRepository(db)
        self.releases_repo = ReleasesRepository(db)
        self.users_repo = UsersRepository(db)

    def add_review(self, request: AddReviewRequest):
        """
        Adds the review and a rating to the database

        - request: the review and rating info
        """
        user = self.users_repo.get_user_by_name(request.user)
        if (user is None):
            raise UsersException("There is no registered user with that name")
        release = self.releases_repo.get_release(request.release_id)
        if (release is None):
            raise ReleasesException("There is no release with that id")
        rating, review = self._create_review_with_rating(request, user.id)
        try:
            self.reviews_repo.new_review_with_rating(review, rating)
        except IntegrityError as ex:
            print(str(ex))
            raise ReviewsException("Review already exists in the database")
        complete_rating = CompleteRating.from_orm(rating)

        complete_review = CompleteReview.from_orm(review)
        # complete_review.rating = complete_rating
        return complete_review

    def get_release_reviews(self, release_id: int, page: int, rowsPerPage: int,
                            order_by: str, order_asc: bool):
        """
        Gets a number of reviews of a release from the database, limited by pages of a limited length,
        and with a possible search text

        - release_id: the id of the release
        - page: the page number, starts from 1
        - rowsPerPage: how many reviews will be in each page
        - order_by: the field the data will be ordered by
        - order_asc: if the data will be sorted in ascending order
        """
        review_list = self.reviews_repo.get_release_reviews(release_id, page, rowsPerPage, order_by, order_asc)
        return [CompleteReview.from_orm(a) for a in review_list]

    def get_user_reviews(self, user: str, page: int, rowsPerPage: int,
                         order_by: str, order_asc: bool):
        """
        Gets a number of reviews of a user from the database, limited by pages of a limited length,
        and with a possible search text

        - user: the name of the user
        - page: the page number, starts from 1
        - rowsPerPage: how many reviews will be in each page
        - order_by: the field the data will be ordered by
        - order_asc: if the data will be sorted in ascending order
        """
        review_list = self.reviews_repo.get_user_reviews(user, page, rowsPerPage, order_by, order_asc)
        return [CompleteReview.from_orm(a) for a in review_list]

    def get_review(self, review_id: int):
        """
        Gets a number of reviews of a certain id from the database, if it doesn't exist, it will return None

        - review_id: the id of the review
        """
        review_orm = self.reviews_repo.get_review(review_id)
        if review_orm is None:
            return None
        return CompleteReview.from_orm(review_orm)

    def update_review(self, review_id: int, request: UpdateReviewRequest):
        """
        Changes the score or content of a review

        - review_id: the id of the review
        - request: the score and/or content of the review that will replace the old one
        """
        review = self.reviews_repo.get_review(review_id)
        if review is None:
            raise ReviewsException("There is no review with that id")
        updated_review = self.reviews_repo.update_review(review_id, request.score, request.content)
        return CompleteReview.from_orm(updated_review)
    
    def delete_review(self, review_id: int):
        """
        Changes the score or content of a review

        - review_id: the id of the review
        """
        review = self.reviews_repo.get_review(review_id)
        if review is None:
            raise ReviewsException("There is no review with that id")
        self.reviews_repo.delete_review(review_id)

    def _create_review_with_rating(self, request: AddReviewRequest, user_id: int):
        rating = Rating.from_request(request, user_id)
        review = Review.from_request(request)
        review.ratings = rating
        return rating, review  # Returning tuple

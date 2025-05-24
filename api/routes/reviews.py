from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import APIKeyHeader
from api.helpers.auth_helper import get_current_user, validate_token
from api.model.requests.reviews_requests import AddReviewRequest, UpdateReviewRequest
from api.model.requests.paging_params import PagingParams
from api.controllers.reviews_controller import ReviewsController
from typing import Annotated, Literal

router = APIRouter(dependencies=[Depends(validate_token)])
api_key_header = APIKeyHeader(name="Authorization")


@router.post("/releases/{release_id}/reviews", status_code=201)
def add_review(request: AddReviewRequest, user: dict = Depends(get_current_user),
               controller: ReviewsController = Depends()):
    """
    [ADMIN ONLY] Adds a new review to a release
    If operation is successful the review is returned

    - **request**: Review Data - the name, artist, the date it's been published, etc.
    """
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Operation restricted for non-admin users")
    return controller.add_review(request)


@router.get("/releases/{release_id}/reviews", status_code=200, responses={204: {"description": "No Content"}})
def get_release_reviews(release_id: int, paging_query: PagingParams = Depends(), order_by: Literal["id"] = id,
                        order_asc: bool = False, controller: ReviewsController = Depends()):
    """
    Gets the reviews added to a certain release, with paging

    - **release_id**: the id of the release.
    - **page**: the reviews page. Must be greater than 0.
    Default value is 1.
    - **rowsPerPage**: how many reviews there will be per page. Must be greater than 0 and at most 1000.
    Default value is 10.
    - **search**: text to search an review by their name.
    - **order_by**: the field the results will be ordered by.
    - **order_asc**: if the data will be sorted in ascending order
    """
    return controller.get_release_reviews(release_id, paging_query.page, paging_query.rowsPerPage,
                                  order_by, order_asc)


@router.get("/user/{user}/reviews", status_code=200, responses={204: {"description": "No Content"}})
def get_user_reviews(user: str, paging_query: PagingParams = Depends(), order_by: Literal["id"] = id,
                     order_asc: bool = False, controller: ReviewsController = Depends()):
    """
    Gets the reviews written by a certain user, with paging

    - **user**: the name of the user.
    - **page**: the reviews page. Must be greater than 0.
    Default value is 1.
    - **rowsPerPage**: how many reviews there will be per page. Must be greater than 0 and at most 1000.
    Default value is 10.
    - **search**: text to search an review by their name.
    - **order_by**: the field the results will be ordered by.
    - **order_asc**: if the data will be sorted in ascending order
    """
    return controller.get_user_reviews(user, paging_query.page, paging_query.rowsPerPage, order_by, order_asc)


@router.get("/reviews/{review_id}", status_code=200)
def get_review(review_id: Annotated[int, Path(
                title="Review id",
                description="The id of the review",
                ge=0)],
               controller: ReviewsController = Depends()):
    """
    Gets the review of a given id.
    
    - **review_id**: Id of the review
    """
    return controller.get_review(review_id)


@router.put("/reviews/{review_id}", status_code=200)
def update_review(review_id: Annotated[int, Path(
                title="Review id",
                description="The id of the review",
                ge=0)],
                request: UpdateReviewRequest,
                controller: ReviewsController = Depends()):
    """
    Updates the content or score (rating) of a review of a given id
    
    - **request**: the score or content of the review that will be added
    - **review_id**: Id of the review
    """
    return controller.update_review(review_id, request)


@router.delete("/reviews/{review_id}", status_code=200)
def delete_review(review_id: Annotated[int, Path(
                title="Review id",
                description="The id of the review",
                ge=0)],
                controller: ReviewsController = Depends()):
    """
    Deletes a review from the database

    - **review_id**: Id of the review
    """
    return controller.delete_review(review_id)

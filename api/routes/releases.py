from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import APIKeyHeader
from api.helpers.auth_helper import get_current_user, validate_token
from api.model.requests.releases_requests import AddReleaseRequest
from api.model.requests.paging_params import PagingParamsSearch
from api.controllers.releases_controller import ReleasesController
from typing import Annotated, Literal

router = APIRouter(dependencies=[Depends(validate_token)])
api_key_header = APIKeyHeader(name="Authorization")


@router.post("/releases", status_code=201)
def add_release(request: AddReleaseRequest, user: dict = Depends(get_current_user),
                controller: ReleasesController = Depends()):
    """
    [ADMIN ONLY] Adds a new release to the database
    If operation is successful the release is returned

    - **request**: Release Data - the name, artist, the date it's been published, etc.
    """
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Operation restricted for non-admin users")
    return controller.add_release(request)


@router.get("/releases", status_code=200, responses={204: {"description": "No Content"}})
def get_releases(paging_query: PagingParamsSearch = Depends(), order_by: Literal["id", "name"] = id, order_asc: bool = False,
                 controller: ReleasesController = Depends()):
    """
    Gets the releases added in the website with paging

    - **page**: the releases page. Must be greater than 0.
    Default value is 1.
    - **rowsPerPage**: how many releases there will be per page. Must be greater than 0 and at most 1000.
    Default value is 10.
    - **search**: text to search an release by their name.
    - **order_by**: the field the results will be ordered by.
    - **order_asc**: if the data will be sorted in ascending order
    """
    return controller.get_releases(paging_query.page, paging_query.rowsPerPage, paging_query.search, order_by,
                                   order_asc)


@router.get("/releases/{release_id}", status_code=200)
def get_release(release_id: Annotated[int, Path(
                title="Release id",
                description="The id of the release",
                ge=0)],
                controller: ReleasesController = Depends()):
    """
    Gets the release of a given id
    - **release_id**: Id of the release
    """
    return controller.get_release(release_id)

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import APIKeyHeader
from api.helpers.auth_helper import get_current_user, validate_token
from api.model.requests.artists_requests import AddArtistRequest
from api.model.requests.paging_params import PagingParamsSearch
from api.controllers.artists_controller import ArtistsController
from typing import Annotated, Literal

router = APIRouter(dependencies=[Depends(validate_token)])
api_key_header = APIKeyHeader(name="Authorization")


@router.post("/artists", status_code=201)
def add_artist(request: AddArtistRequest, user: dict = Depends(get_current_user),
               controller: ArtistsController = Depends()):
    """
    [ADMIN ONLY] Adds a new artist to the database
    If operation is successful the artist is returned

    - **request**: Artist Data - the name, country of origin, the date it's been active since, etc.
    """
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Operation restricted for non-admin users")
    return controller.add_artist(request)


@router.get("/artists", status_code=200, responses={204: {"description": "No Content"}})
def get_artists(paging_query: PagingParamsSearch = Depends(),
                order_by: Literal["id", "name"] = id,
                order_asc: bool = False,
                controller: ArtistsController = Depends()):
    """
    Gets the artists added in the website with paging

    - **page**: the artists page. Must be greater than 0.
    Default value is 1.
    - **rowsPerPage**: how many artists there will be per page. Must be greater than 0 and at most 1000.
    Default value is 10.
    - **search**: text to search an artist by their name.
    - **order_by**: the field the results will be ordered by.
    - **order_asc**: if the data will be sorted in ascending order
    """
    return controller.get_artists(paging_query.page,
                                  paging_query.rowsPerPage,
                                  paging_query.search,
                                  order_by,
                                  order_asc)


@router.get("/artists/{artist_id}", status_code=200)
def get_artist(artist_id: Annotated[int, Path(
                title="Artist id",
                description="The id of the artist",
                ge=0)],
               controller: ArtistsController = Depends()):
    """
    Gets the artist of a given id
    - **artist_id**: Id of the artist
    """
    return controller.get_artist(artist_id)

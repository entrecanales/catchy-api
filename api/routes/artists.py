from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from api.helpers.auth_helper import get_current_user
from api.model.requests.artists_requests import AddArtistRequest
from api.controllers.artists_controller import ArtistsController

router = APIRouter()
api_key_header = APIKeyHeader(name="Authorization")


@router.post("/artists", status_code=201)
def add_artist(request: AddArtistRequest, token: str = Security(api_key_header),
               controller: ArtistsController = Depends()):
    """
    [ADMIN ONLY] Adds a new artist to the database
    If operation is successful the artist is returned

    - **request**: Artist Data - the name, country of origin, the date it's been active since, etc.
    """
    user = get_current_user(token)
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Operation restricted for non-admin users")
    return controller.add_artist(request)

'''
@router.get("/artists", status_code=200)
def get_artists(request: RegisterRequest, controller: AuthenticationController = Depends()):
    """
    Register a user given username, password, email and profile data

    Sends an email to the given address in order to complete the process
    - **request**: User Data - the username, password, email, display name, etc.
    """
    return controller.register(request)


@router.get("/artists/{artist_id}", status_code=200)
def get_artist(artist_id: int, controller: AuthenticationController = Depends()):
    """
    Register a user given username, password, email and profile data

    Sends an email to the given address in order to complete the process
    - **request**: User Data - the username, password, email, display name, etc.
    """
    return controller.register(request)
'''

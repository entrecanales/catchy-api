from fastapi import APIRouter, Depends, Security
from fastapi.security import APIKeyHeader
from api.controllers.authentication_controller import AuthenticationController
from api.model.requests.authentication_requests import RegisterRequest, LoginRequest


router = APIRouter()
api_key_header = APIKeyHeader(name="Authorization")


@router.post("/register", status_code=201)
def register(request: RegisterRequest, controller: AuthenticationController = Depends()):
    """
    Register a user given username, password, email and profile data

    Sends an email to the given address in order to complete the process
    - **request**: User Data - the username, password, email, display name, etc.
    """
    return controller.register(request)


@router.post("/login")
def login(request: LoginRequest, controller: AuthenticationController = Depends()):
    """
    Gets a JWT token for a user, given its password was indicated correctly

    - **request**: Username and password
    """
    return controller.login(request)


@router.get("/me")
def me(token: str = Security(api_key_header), controller: AuthenticationController = Depends()):
    """
    Gets an user from a valid JWT token

    - **token**: JWT token
    """
    return controller.me(token)

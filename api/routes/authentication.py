from fastapi import APIRouter, Depends
from api.controllers.authentication_controller import AuthenticationController
from api.model.requests.authentication_requests import RegisterRequest


router = APIRouter()


# TODO: This send an email to the address to confim and needs to store the password ENCRYPTED
@router.post("/register", status_code=201)
def register(request: RegisterRequest, controller: AuthenticationController = Depends()):
    return controller.register(request)


@router.post("/login")  # TODO: This needs to return a JWT token
def login(controller: AuthenticationController = Depends()):
    return controller.login()


@router.get("/me")
def me(controller: AuthenticationController = Depends()):
    return controller.me()

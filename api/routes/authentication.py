from fastapi import APIRouter, Depends
from api.controllers.authentication_controller import AuthenticationController
from api.model.requests.authentication_requests import RegisterRequest, LoginRequest


router = APIRouter()


@router.post("/register", status_code=201)  # TODO: Add logging
def register(request: RegisterRequest, controller: AuthenticationController = Depends()):
    return controller.register(request)


@router.post("/login")  # TODO: This needs to return a JWT token
def login(request: LoginRequest, controller: AuthenticationController = Depends()):
    return controller.login(request)


@router.get("/me")
def me(controller: AuthenticationController = Depends()):
    return controller.me()

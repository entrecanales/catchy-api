from fastapi import APIRouter, Depends
from api.controllers.authentication_controller import AuthenticationController
from api.model.requests.authentication_requests import RegisterRequest


router = APIRouter()


@router.post("/register")
def register(request: RegisterRequest, controller: AuthenticationController = Depends()):
    return controller.register(request)


@router.post("/login")
def login(controller: AuthenticationController = Depends()):
    return controller.login()


@router.get("/me")
def me(controller: AuthenticationController = Depends()):
    return controller.me()

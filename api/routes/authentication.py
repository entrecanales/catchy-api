from fastapi import APIRouter
from api.controllers.authentication_controller import AuthenticationController
from api.services.authentication_service import AuthenticationService

router = APIRouter()
controller = AuthenticationController(service=AuthenticationService())


@router.post("/register")
def register():
    return controller.register()


@router.post("/login")
def login():
    return controller.login()


@router.get("/me")
def me():
    return controller.me()

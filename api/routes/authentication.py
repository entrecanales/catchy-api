from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.controllers.authentication_controller import AuthenticationController
from api.services.authentication_service import AuthenticationService
from api.model.requests.authentication_requests import RegisterRequest
from core.db import get_db


router = APIRouter()
controller = AuthenticationController(service=AuthenticationService())


@router.post("/register")
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    return controller.register(request, db)


@router.post("/login")
def login():
    return controller.login()


@router.get("/me")
def me():
    return controller.me()

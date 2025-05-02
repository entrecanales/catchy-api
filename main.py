from fastapi import FastAPI
from api.routes.authentication import router as authentication_router


app = FastAPI()
app.include_router(authentication_router, prefix="/api/v1/authentication")

from fastapi import FastAPI
from api.routes.authentication import router as authentication_router
from api.routes.artists import router as artists_router


app = FastAPI()
app.include_router(authentication_router, prefix="/api/v1/authentication")
app.include_router(artists_router, prefix="/api/v1/artists")

from core.db import get_db
from core.logger import get_logger
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from api.services.artists_service import ArtistsService
from api.model.requests.artists_requests import AddArtistRequest
from api.model.exceptions.artists_exception import ArtistsException
import uuid


class ArtistsController:
    def __init__(self, db: Session = Depends(get_db)):
        self.service = ArtistsService(db)
        self.logger = get_logger('catchy')

    def add_artist(self, request: AddArtistRequest):
        """
        [ADMIN ONLY] Adds a new artist to the database.
        If operation is successful the artist is returned

        - request: the artist data
        """
        try:
            return self.service.add_artist(request)
        except ArtistsException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

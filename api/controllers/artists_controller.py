from core.db import get_db
from core.logger import get_logger
from fastapi import HTTPException, Depends, Response
from sqlalchemy.orm import Session
from api.services.artists_service import ArtistsService
from api.model.requests.artists_requests import AddArtistRequest
from api.model.exceptions.artists_exception import ArtistsException
from typing import Literal
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

    def get_artists(self,
                    page: int,
                    rowsPerPage: int,
                    search: str | None,
                    order_by: Literal["id", "name"],
                    order_asc: bool):
        """
        Gets the artists added in the website with paging

        - **page**: the artists page
        - **rowsPerPage**: how many artists there will be per page
        - **search**: text to search an artist by their name
        - **order_by**: the field the results will be ordered by.
        - **order_asc**: if the data will be sorted in ascending order
        """
        # Data validation
        if isinstance(search, str) and not search:  # error if the search text isn't null but is empty
            raise HTTPException(status_code=400, detail="The search text, if not null, must not be empty")
        # Logic
        try:
            artists = self.service.get_artists(page, rowsPerPage, search, order_by, order_asc)
            if len(artists) == 0:
                return Response(status_code=204)
        except ArtistsException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

    def get_artist(self, artist_id: int):
        """
        Gets an artist of a certain id

        - **artist_id**: id of an artist
        """
        # Logic
        try:
            artist = self.service.get_artist(artist_id)
            if artist is not None:
                return artist
        except ArtistsException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")
        raise HTTPException(status_code=404, detail="Not Found")

from core.db import get_db
from core.logger import get_logger
from fastapi import HTTPException, Depends, Response
from sqlalchemy.orm import Session
from api.services.releases_service import ReleasesService
from api.model.requests.releases_requests import AddReleaseRequest
from api.model.exceptions.business_exception import BusinessException
from typing import Literal
import uuid


class ReleasesController:
    def __init__(self, db: Session = Depends(get_db)):
        self.service = ReleasesService(db)
        self.logger = get_logger('catchy')

    def add_release(self, request: AddReleaseRequest):
        """
        [ADMIN ONLY] Adds a new release to the database.
        If operation is successful the release is returned

        - request: the release data
        """
        try:
            return self.service.add_release(request)
        except BusinessException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

    def get_releases(self,
                     page: int,
                     rowsPerPage: int,
                     search: str | None,
                     order_by: Literal["id", "name"],
                     order_asc: bool):
        """
        Gets the releases added in the website with paging

        - **page**: the releases page
        - **rowsPerPage**: how many releases there will be per page
        - **search**: text to search an release by their name
        - **order_by**: the field the results will be ordered by.
        - **order_asc**: if the data will be sorted in ascending order
        """
        # Data validation
        if isinstance(search, str) and not search:  # error if the search text isn't null but is empty
            raise HTTPException(status_code=400, detail="The search text, if not null, must not be empty")
        # Logic
        try:
            releases = self.service.get_releases(page, rowsPerPage, search, order_by, order_asc)
            if len(releases) == 0:
                return Response(status_code=204)
            return releases
        except BusinessException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")

    def get_release(self, release_id: int):
        """
        Gets an release of a certain id

        - **release_id**: id of an release
        """
        # Logic
        try:
            release = self.service.get_release(release_id)
            if release is not None:
                return release
        except BusinessException as ex:
            raise HTTPException(status_code=400, detail=str(ex))
        except Exception as ex:
            error_uuid = str(uuid.uuid4())
            self.logger.error(f"[UUID - {error_uuid}] {ex}")
            raise HTTPException(status_code=500, detail="Oops! Something went wrong. Contact an administrator " +
                                f"and give them this reference number: {error_uuid}")
        raise HTTPException(status_code=404, detail="Not Found")

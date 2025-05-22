from api.model.requests.releases_requests import AddReleaseRequest
from api.model.entities.generated_models import Releases as Release
from api.model.schemas.releases_schemas import CompleteRelease
from api.model.exceptions.releases_exception import ReleasesException
from api.repositories.releases_repo import ReleasesRepository
from sqlalchemy.exc import IntegrityError


class ReleasesService:
    def __init__(self, db):
        self.releases_repo = ReleasesRepository(db)

    def add_release(self, request: AddReleaseRequest):
        """
        Adds the release to the database

        - request: the release info
        """
        release = Release.from_request(request)
        try:
            self.releases_repo.new_release(release)
        except IntegrityError:
            raise ReleasesException("Release already exists in the database")
        return CompleteRelease.from_orm(release)

    def get_releases(self, page: int, rowsPerPage: int, search: str | None, order_by: str, order_asc: bool):
        """
        Gets a number of releases from the database, limited by pages of a limited length,
        and with a possible search text

        - page: the page number, starts from 1
        - rowsPerPage: how many releases will be in each page
        - search: an optional text to search releases by name
        - order_by: the field the data will be ordered by
        - order_asc: if the data will be sorted in ascending order
        """
        release_list = self.releases_repo.get_releases(page, rowsPerPage, search, order_by, order_asc)
        return [CompleteRelease.from_orm(a) for a in release_list]

    def get_release(self, release_id: int):
        """
        Gets a number of releases of a certain id from the database, if it doesn't exist, it will return None

        - release_id: the id of the release
        """
        release_orm = self.releases_repo.get_release(release_id)
        if release_orm is None:
            return None
        return CompleteRelease.from_orm(release_orm)

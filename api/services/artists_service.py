from api.model.requests.artists_requests import AddArtistRequest
from api.model.entities.generated_models import Artists as Artist
from api.model.schemas.artists_schemas import AddedArtist
from api.model.exceptions.artists_exception import ArtistsException
from api.repositories.artists_repo import ArtistsRepository
from sqlalchemy.exc import IntegrityError


class ArtistsService:
    def __init__(self, db):
        self.artists_repo = ArtistsRepository(db)

    def add_artist(self, request: AddArtistRequest):
        """
        Adds the artist to the database

        - request: the artist info
        """
        artist = Artist.from_request(request)
        try:
            self.artists_repo.new_artist(artist)
        except IntegrityError:
            raise ArtistsException("Artist already exists in the database")
        return AddedArtist.from_orm(artist)

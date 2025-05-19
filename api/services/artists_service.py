from api.model.requests.artists_requests import AddArtistRequest
from api.model.entities.generated_models import Artists as Artist
from api.model.schemas.artists_schemas import CompleteArtist, SimpleArtist
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
        return CompleteArtist.from_orm(artist)

    def get_artists(self, page: int, rowsPerPage: int, search: str | None, order_by: str, order_asc: bool):
        """
        Gets a number of artists from the database, limited by pages of a limited length,
        and with a possible search text

        - page: the page number, starts from 1
        - rowsPerPage: how many artists will be in each page
        - search: an optional text to search artists by name
        - order_by: the field the data will be ordered by
        - order_asc: if the data will be sorted in ascending order
        """
        artist_list = self.artists_repo.get_artists(page, rowsPerPage, search, order_by, order_asc)
        return [SimpleArtist.from_orm(a) for a in artist_list]

    def get_artist(self, artist_id: int):
        """
        Gets a number of artists of a certain id from the database, if it doesn't exist, it will return None

        - artist_id: the id of the artist
        """
        artist_orm = self.artists_repo.get_artist(artist_id)
        if artist_orm is None:
            return None
        return CompleteArtist.from_orm(artist_orm)

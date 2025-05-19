from sqlalchemy import text
from sqlalchemy.orm import Session
from api.model.entities.generated_models import Artists as Artist
from api.helpers import model_helper as ModelHelper
from datetime import datetime, timezone
from typing import Literal


class ArtistsRepository:
    def __init__(self, db: Session):
        self.db = db

    def new_artist(self, artist: Artist):
        """
        Adds a new artist into the database
        """
        # initialize the created_at to now, the time and date of the operation
        artist.created_at = datetime.now(tz=timezone.utc)
        artist.updated_at = datetime.now(tz=timezone.utc)
        artist_dict = ModelHelper.model_to_dict(artist)
        sql = text("""
            with added_artist as (
                INSERT INTO artists (
                    name, also_known_as, active_since, inactive_since, country,
                    official_website, spotify_url, is_group, created_at, updated_at
                    )
                    VALUES (
                        :name, :also_known_as, :active_since, :inactive_since, :country,
                        :official_website, :spotify_url, :is_group, :created_at, :updated_at
                    )
                RETURNING id
            )
            SELECT id FROM added_artist --Return inserted artists_id
            """)
        result = self.db.execute(sql, artist_dict)
        self.db.commit()
        artist.id = result.fetchone().id
        return artist

    def get_artists(self,
                    page: int,
                    rowsPerPage: int,
                    search: str | None,
                    order_by: Literal["id", "name"],
                    order_asc: bool):
        """
        Gets a number of artists from the database
        """
        sql = text(f"""
            SELECT id, name
            FROM artists
            WHERE :search IS NULL OR name ILIKE :search --ILIKE because it's case insensitive
            ORDER BY {order_by} {'ASC' if order_asc else 'DESC'}
            LIMIT :limit OFFSET :offset
            """)

        params_dict = {
            'offset': (page - 1) * rowsPerPage,
            'limit': rowsPerPage,
            'asc': 'ASC' if order_asc else "DESC",
            'search': f"%{search}%" if search else None
        }

        result = self.db.execute(sql, params_dict)
        return result.fetchall()

    def get_artist(self, artist_id: int):
        """
        Gets an artist from the database
        """
        sql = text("""
            SELECT id, name, also_known_as, active_since, inactive_since,
            country, official_website, spotify_url, is_group, created_at, updated_at
            FROM artists
            WHERE id = :artist_id
            """)

        result = self.db.execute(sql, {'artist_id': artist_id})
        return result.fetchone()

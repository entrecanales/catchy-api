from sqlalchemy import text
from sqlalchemy.orm import Session
from api.model.entities.generated_models import Releases as Release
from api.helpers import model_helper as ModelHelper
from datetime import datetime, timezone
from typing import Literal


class ReleasesRepository:
    def __init__(self, db: Session):
        self.db = db

    def new_release(self, release: Release):
        """
        Adds a new release into the database
        """
        # initialize the created_at to now, the time and date of the operation
        release.created_at = datetime.now(tz=timezone.utc)
        release.updated_at = datetime.now(tz=timezone.utc)
        release_dict = ModelHelper.model_to_dict(release)
        sql = text("""
            with added_release as (
                INSERT INTO releases (
                    name, type, release_date, language, created_at, updated_at
                    )
                    VALUES (
                        :name, :type, :release_date, :language, :created_at, :updated_at
                    )
                RETURNING id
            )
            SELECT id FROM added_release --Return inserted releases_id
            """)
        result = self.db.execute(sql, release_dict)
        release.id = result.fetchone().id
        intermdiate_sql = text("""
                    INSERT INTO release_artist (
                        artist_fk, release_fk, release_name
                        )
                    VALUES (
                        :artist_fk, :release_fk, :release_name
                    )
                    """)
        self.db.execute(intermdiate_sql, {"artist_fk": release.artist,
                                          "release_fk": release.id,
                                          "release_name": release.name})
        self.db.commit()
        return release

    def get_releases(self,
                     page: int,
                     rowsPerPage: int,
                     search: str | None,
                     order_by: Literal["id", "name"],
                     order_asc: bool):
        """
        Gets a number of releases from the database
        """
        sql = text(f"""
            SELECT r.id, r.name, r.type, r.release_date, r.language, ra.artist_fk as artist_id
            FROM releases r INNER JOIN release_artist ra ON r.id = ra.release_fk
            WHERE :search IS NULL OR r.name ILIKE :search --ILIKE because it's case insensitive
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

    def get_release(self, release_id: int):
        """
        Gets an release from the database
        """
        sql = text("""
            SELECT r.id, r.name, r.type, r.release_date, r.language, r.created_at, r.updated_at, ra.artist_fk as artist_id
            FROM releases r INNER JOIN release_artist ra ON r.id = ra.release_fk
            WHERE r.id = :release_id
            """)

        result = self.db.execute(sql, {'release_id': release_id})
        return result.fetchone()

from typing import List, Optional

from sqlalchemy import Boolean, CHAR, CheckConstraint, Column, Date, DateTime, ForeignKeyConstraint, Identity, Integer, PrimaryKeyConstraint, String, Table, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Artists(Base):
    __tablename__ = 'artists'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='artists_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    also_known_as: Mapped[Optional[str]] = mapped_column(Text)
    active_since: Mapped[Optional[str]] = mapped_column(CHAR(4))
    inactive_since: Mapped[Optional[str]] = mapped_column(CHAR(4))
    country: Mapped[Optional[str]] = mapped_column(String(50))
    official_website: Mapped[Optional[str]] = mapped_column(Text)
    spotify_url: Mapped[Optional[str]] = mapped_column(Text)
    is_group: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    genre: Mapped[List['Genre']] = relationship('Genre', secondary='artist_genre', back_populates='artists')
    tracks: Mapped[List['Tracks']] = relationship('Tracks', secondary='artist_tracks', back_populates='artists')
    users: Mapped[List['Users']] = relationship('Users', secondary='favorite_artists', back_populates='artists')
    artists: Mapped[List['Artists']] = relationship('Artists', secondary='member_of', primaryjoin=lambda: Artists.id == t_member_of.c.band_fk, secondaryjoin=lambda: Artists.id == t_member_of.c.member_fk, back_populates='artists_')
    artists_: Mapped[List['Artists']] = relationship('Artists', secondary='member_of', primaryjoin=lambda: Artists.id == t_member_of.c.member_fk, secondaryjoin=lambda: Artists.id == t_member_of.c.band_fk, back_populates='artists')
    artist_tags: Mapped[List['ArtistTags']] = relationship('ArtistTags', back_populates='artists')


class Genre(Base):
    __tablename__ = 'genre'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='genre_pkey'),
        UniqueConstraint('name', name='genre_name_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    artists: Mapped[List['Artists']] = relationship('Artists', secondary='artist_genre', back_populates='genre')
    releases: Mapped[List['Releases']] = relationship('Releases', secondary='release_genre', back_populates='genre')


class Releases(Base):
    __tablename__ = 'releases'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='releases_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[Optional[str]] = mapped_column(String(10))
    release_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    language: Mapped[Optional[str]] = mapped_column(String(20))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    genre: Mapped[List['Genre']] = relationship('Genre', secondary='release_genre', back_populates='releases')
    users: Mapped[List['Users']] = relationship('Users', secondary='favorite_releases', back_populates='releases')
    tracks: Mapped[List['Tracks']] = relationship('Tracks', secondary='release_tracks', back_populates='releases')
    ratings: Mapped[List['Ratings']] = relationship('Ratings', back_populates='releases')


class Tracks(Base):
    __tablename__ = 'tracks'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='tracks_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    release_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True))
    duration: Mapped[Optional[datetime.timedelta]] = mapped_column(INTERVAL)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    artists: Mapped[List['Artists']] = relationship('Artists', secondary='artist_tracks', back_populates='tracks')
    releases: Mapped[List['Releases']] = relationship('Releases', secondary='release_tracks', back_populates='tracks')
    user_list_tracks: Mapped[List['UserListTracks']] = relationship('UserListTracks', back_populates='tracks')


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        UniqueConstraint('email', name='users_email_key'),
        UniqueConstraint('username', name='users_username_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    pass_: Mapped[str] = mapped_column('pass', Text)
    email: Mapped[str] = mapped_column(String(100))
    display_name: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[datetime.date] = mapped_column(Date)
    gender: Mapped[str] = mapped_column(String(16))
    timezone: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    location: Mapped[Optional[str]] = mapped_column(String(100))
    about: Mapped[Optional[str]] = mapped_column(String(500))
    website: Mapped[Optional[str]] = mapped_column(String(100))
    picture_url: Mapped[Optional[str]] = mapped_column(Text)

    artists: Mapped[List['Artists']] = relationship('Artists', secondary='favorite_artists', back_populates='users')
    releases: Mapped[List['Releases']] = relationship('Releases', secondary='favorite_releases', back_populates='users')
    follower: Mapped[List['Users']] = relationship('Users', secondary='users_follows', primaryjoin=lambda: Users.id == t_users_follows.c.followed_id, secondaryjoin=lambda: Users.id == t_users_follows.c.follower_id, back_populates='followed')
    followed: Mapped[List['Users']] = relationship('Users', secondary='users_follows', primaryjoin=lambda: Users.id == t_users_follows.c.follower_id, secondaryjoin=lambda: Users.id == t_users_follows.c.followed_id, back_populates='follower')
    ratings: Mapped[List['Ratings']] = relationship('Ratings', back_populates='users')
    user_comment: Mapped[List['UserComment']] = relationship('UserComment', foreign_keys='[UserComment.author_fk]', back_populates='users')
    user_comment_: Mapped[List['UserComment']] = relationship('UserComment', foreign_keys='[UserComment.user_profile_fk]', back_populates='users_')
    user_lists: Mapped[List['UserLists']] = relationship('UserLists', back_populates='users')


t_artist_genre = Table(
    'artist_genre', Base.metadata,
    Column('artist_fk', Integer, primary_key=True, nullable=False),
    Column('genre_fk', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['artist_fk'], ['artists.id'], ondelete='CASCADE', name='artist_genre_artist_fk_fkey'),
    ForeignKeyConstraint(['genre_fk'], ['genre.id'], ondelete='CASCADE', name='artist_genre_genre_fk_fkey'),
    PrimaryKeyConstraint('artist_fk', 'genre_fk', name='artist_genre_pkey')
)


class ArtistTags(Base):
    __tablename__ = 'artist_tags'
    __table_args__ = (
        ForeignKeyConstraint(['artist_fk'], ['artists.id'], ondelete='CASCADE', name='artist_tags_artist_fk_fkey'),
        PrimaryKeyConstraint('id', name='artist_tags_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    tag_content: Mapped[str] = mapped_column(String(100))
    artist_fk: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    artists: Mapped['Artists'] = relationship('Artists', back_populates='artist_tags')


t_artist_tracks = Table(
    'artist_tracks', Base.metadata,
    Column('artist_fk', Integer, primary_key=True, nullable=False),
    Column('track_fk', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['artist_fk'], ['artists.id'], ondelete='CASCADE', name='artist_tracks_artist_fk_fkey'),
    ForeignKeyConstraint(['track_fk'], ['tracks.id'], ondelete='CASCADE', name='artist_tracks_track_fk_fkey'),
    PrimaryKeyConstraint('artist_fk', 'track_fk', name='artist_tracks_pkey')
)


t_favorite_artists = Table(
    'favorite_artists', Base.metadata,
    Column('artist_fk', Integer, primary_key=True, nullable=False),
    Column('user_fk', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['artist_fk'], ['artists.id'], ondelete='CASCADE', name='favorite_artists_artist_fk_fkey'),
    ForeignKeyConstraint(['user_fk'], ['users.id'], ondelete='CASCADE', name='favorite_artists_user_fk_fkey'),
    PrimaryKeyConstraint('artist_fk', 'user_fk', name='favorite_artists_pkey')
)


t_favorite_releases = Table(
    'favorite_releases', Base.metadata,
    Column('release_fk', Integer, primary_key=True, nullable=False),
    Column('user_fk', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['release_fk'], ['releases.id'], ondelete='CASCADE', name='favorite_releases_release_fk_fkey'),
    ForeignKeyConstraint(['user_fk'], ['users.id'], ondelete='CASCADE', name='favorite_releases_user_fk_fkey'),
    PrimaryKeyConstraint('release_fk', 'user_fk', name='favorite_releases_pkey')
)


t_member_of = Table(
    'member_of', Base.metadata,
    Column('band_fk', Integer, primary_key=True, nullable=False),
    Column('member_fk', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['band_fk'], ['artists.id'], ondelete='CASCADE', name='member_of_band_fk_fkey'),
    ForeignKeyConstraint(['member_fk'], ['artists.id'], ondelete='CASCADE', name='member_of_member_fk_fkey'),
    PrimaryKeyConstraint('band_fk', 'member_fk', name='member_of_pkey')
)


class Ratings(Base):
    __tablename__ = 'ratings'
    __table_args__ = (
        CheckConstraint('score >= 0 AND score <= 100', name='ratings_score_check'),
        ForeignKeyConstraint(['release_fk'], ['releases.id'], ondelete='CASCADE', name='ratings_release_fk_fkey'),
        ForeignKeyConstraint(['user_fk'], ['users.id'], ondelete='CASCADE', name='ratings_user_fk_fkey'),
        PrimaryKeyConstraint('id', name='ratings_pkey'),
        UniqueConstraint('user_fk', 'release_fk', name='ratings_user_fk_release_fk_key')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    user_fk: Mapped[int] = mapped_column(Integer)
    release_fk: Mapped[int] = mapped_column(Integer)
    score: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    releases: Mapped['Releases'] = relationship('Releases', back_populates='ratings')
    users: Mapped['Users'] = relationship('Users', back_populates='ratings')
    reviews: Mapped[List['Reviews']] = relationship('Reviews', back_populates='ratings')


t_release_genre = Table(
    'release_genre', Base.metadata,
    Column('release_fk', Integer, primary_key=True, nullable=False),
    Column('genre_fk', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['genre_fk'], ['genre.id'], ondelete='CASCADE', name='release_genre_genre_fk_fkey'),
    ForeignKeyConstraint(['release_fk'], ['releases.id'], ondelete='CASCADE', name='release_genre_release_fk_fkey'),
    PrimaryKeyConstraint('release_fk', 'genre_fk', name='release_genre_pkey')
)


t_release_tracks = Table(
    'release_tracks', Base.metadata,
    Column('release_fk', Integer, primary_key=True, nullable=False),
    Column('track_fk', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['release_fk'], ['releases.id'], ondelete='CASCADE', name='release_tracks_release_fk_fkey'),
    ForeignKeyConstraint(['track_fk'], ['tracks.id'], ondelete='CASCADE', name='release_tracks_track_fk_fkey'),
    PrimaryKeyConstraint('release_fk', 'track_fk', name='release_tracks_pkey')
)


class UserComment(Base):
    __tablename__ = 'user_comment'
    __table_args__ = (
        ForeignKeyConstraint(['author_fk'], ['users.id'], ondelete='CASCADE', name='user_comment_author_fk_fkey'),
        ForeignKeyConstraint(['user_profile_fk'], ['users.id'], ondelete='CASCADE', name='user_comment_user_profile_fk_fkey'),
        PrimaryKeyConstraint('id', name='user_comment_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    content: Mapped[str] = mapped_column(String(500))
    author_fk: Mapped[int] = mapped_column(Integer)
    user_profile_fk: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    users: Mapped['Users'] = relationship('Users', foreign_keys=[author_fk], back_populates='user_comment')
    users_: Mapped['Users'] = relationship('Users', foreign_keys=[user_profile_fk], back_populates='user_comment_')


class UserLists(Base):
    __tablename__ = 'user_lists'
    __table_args__ = (
        ForeignKeyConstraint(['user_fk'], ['users.id'], ondelete='CASCADE', name='user_lists_user_fk_fkey'),
        PrimaryKeyConstraint('id', name='user_lists_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    user_fk: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    users: Mapped['Users'] = relationship('Users', back_populates='user_lists')
    user_list_tracks: Mapped[List['UserListTracks']] = relationship('UserListTracks', back_populates='user_lists')


t_users_follows = Table(
    'users_follows', Base.metadata,
    Column('follower_id', Integer, primary_key=True, nullable=False),
    Column('followed_id', Integer, primary_key=True, nullable=False),
    ForeignKeyConstraint(['followed_id'], ['users.id'], ondelete='CASCADE', name='users_follows_followed_id_fkey'),
    ForeignKeyConstraint(['follower_id'], ['users.id'], ondelete='CASCADE', name='users_follows_follower_id_fkey'),
    PrimaryKeyConstraint('follower_id', 'followed_id', name='users_follows_pkey')
)


class Reviews(Base):
    __tablename__ = 'reviews'
    __table_args__ = (
        ForeignKeyConstraint(['rating_fk'], ['ratings.id'], ondelete='CASCADE', name='reviews_rating_fk_fkey'),
        PrimaryKeyConstraint('id', name='reviews_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, Identity(always=True, start=1, increment=1, minvalue=1, maxvalue=2147483647, cycle=False, cache=1), primary_key=True)
    content: Mapped[str] = mapped_column(String(1000))
    rating_fk: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))

    ratings: Mapped['Ratings'] = relationship('Ratings', back_populates='reviews')


class UserListTracks(Base):
    __tablename__ = 'user_list_tracks'
    __table_args__ = (
        ForeignKeyConstraint(['list_fk'], ['user_lists.id'], ondelete='CASCADE', name='user_list_tracks_list_fk_fkey'),
        ForeignKeyConstraint(['track_fk'], ['tracks.id'], ondelete='CASCADE', name='user_list_tracks_track_fk_fkey'),
        PrimaryKeyConstraint('list_fk', 'track_fk', name='user_list_tracks_pkey')
    )

    list_fk: Mapped[int] = mapped_column(Integer, primary_key=True)
    track_fk: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[Optional[str]] = mapped_column(String(500))

    user_lists: Mapped['UserLists'] = relationship('UserLists', back_populates='user_list_tracks')
    tracks: Mapped['Tracks'] = relationship('Tracks', back_populates='user_list_tracks')

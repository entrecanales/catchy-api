-- User Table
CREATE TABLE users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password TEXT NOT NULL, -- Use hashed passwords
    email VARCHAR(100) NOT NULL UNIQUE, --if your email is longer than 99 chars you're a psycho
    display_name VARCHAR(100) NOT NULL,
    gender VARCHAR(16) NOT NULL,
    timezone VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(), --TIMESTAMPZ = timezone aware timestamp
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    is_admin BOOLEAN DEFAULT 0 NOT NULL,
    location VARCHAR(100),
    about VARCHAR(500), --let's be concise, 500 is more than enough
    website VARCHAR(100),
    picture_url TEXT
);

-- User Follows
CREATE TABLE users_follows (
    follower_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    followed_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY(follower_id, followed_id)
);

-- User Comments
CREATE TABLE user_comment (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content VARCHAR(500) NOT NULL,
    author_fk INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    user_profile_fk INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Genres
CREATE TABLE genre (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Artists
CREATE TABLE artists (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    also_known_as TEXT,
    active_since CHAR(4), --char(4) = a year like 2001, 1984 or even 764
    inactive_since CHAR(4),
    country VARCHAR(50),
    official_website TEXT,
    spotify_url TEXT,
    is_group BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Artist Tags
CREATE TABLE artist_tags (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    tag_content VARCHAR(100) NOT NULL,
    artist_fk INT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Artist Genres
CREATE TABLE artist_genre (
    artist_fk INT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
    genre_fk INT NOT NULL REFERENCES genre(id) ON DELETE CASCADE,
    PRIMARY KEY(artist_fk, genre_fk)
);

-- Member of (band members)
CREATE TABLE member_of (
    band_fk INT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
    member_fk INT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
    PRIMARY KEY(band_fk, member_fk)
);

-- Releases
CREATE TABLE releases (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(10), --Album, EP, Single... Could use an FK but I cba
    release_date TIMESTAMPTZ,
    language VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Releases Artist
CREATE TABLE release_artist (
    artist_fk INT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
    release_fk INT NOT NULL REFERENCES releases(id) ON DELETE CASCADE,
    release_name VARCHAR(100) NOT NULL, --Redundant Column to force a unique constraint
    UNIQUE (artist_fk, release_name)
    PRIMARY KEY(artist_fk, release_fk)
);

-- Tracks
CREATE TABLE tracks (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    release_date TIMESTAMPTZ,
    duration INTERVAL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Artist Tracks
CREATE TABLE artist_tracks (
    artist_fk INT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
    track_fk INT NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    PRIMARY KEY(artist_fk, track_fk)
);

-- Release Tracks
CREATE TABLE release_tracks (
    release_fk INT NOT NULL REFERENCES releases(id) ON DELETE CASCADE,
    track_fk INT NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    PRIMARY KEY(release_fk, track_fk)
);

-- Release Genres
CREATE TABLE release_genre (
    release_fk INT NOT NULL REFERENCES releases(id) ON DELETE CASCADE,
    genre_fk INT NOT NULL REFERENCES genre(id) ON DELETE CASCADE,
    PRIMARY KEY(release_fk, genre_fk)
);

-- Favorite Releases
CREATE TABLE favorite_releases (
    release_fk INT NOT NULL REFERENCES releases(id) ON DELETE CASCADE,
    user_fk INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY(release_fk, user_fk)
);

-- Favorite Artists
CREATE TABLE favorite_artists (
    artist_fk INT NOT NULL REFERENCES artists(id) ON DELETE CASCADE,
    user_fk INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    PRIMARY KEY(artist_fk, user_fk)
);

-- User Lists
CREATE TABLE user_lists (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_fk INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- User List Tracks
CREATE TABLE user_list_tracks (
    list_fk INT NOT NULL REFERENCES user_lists(id) ON DELETE CASCADE,
    track_fk INT NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    comment VARCHAR(500),
    PRIMARY KEY(list_fk, track_fk)
);

-- Ratings
CREATE TABLE ratings (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_fk INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    release_fk INT NOT NULL REFERENCES releases(id) ON DELETE CASCADE,
    score INT NOT NULL CHECK(score BETWEEN 0 AND 100), --0 to 100
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_fk, release_fk)
);

-- Reviews
CREATE TABLE reviews (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content VARCHAR(1000) NOT NULL,
    rating_fk INT NOT NULL REFERENCES ratings(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

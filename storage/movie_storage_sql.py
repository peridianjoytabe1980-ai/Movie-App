from sqlalchemy import create_engine, text
import requests

engine = create_engine("sqlite:///movies.db")

with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER,
            rating REAL,
            poster TEXT
        )
    """))
    connection.commit()


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating, poster FROM movies"))
        movies = result.fetchall()

    return {
        row[0]: {"year": row[1], "rating": row[2], "poster": row[3]}
        for row in movies
    }


def add_movie(title):
    """Add a new movie to the database using OMDb API."""
    OMDB_API_KEY = "621a1d46"
    OMDB_URL = "https://www.omdbapi.com/"

    try:
        response = requests.get(OMDB_URL, params={"t": title, "apikey": OMDB_API_KEY})
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "False":
            print(f"Movie '{title}' not found in OMDb.")
            return

        movie_title = data.get("Title")
        year = data.get("Year")
        rating = data.get("imdbRating")
        poster = data.get("Poster")

        with engine.begin() as connection:
            # ✅ Case-insensitive check for existing title
            existing = connection.execute(
                text("SELECT 1 FROM movies WHERE lower(title) = lower(:title)"),
                {"title": movie_title}
            ).fetchone()

            if existing:
                print(f"Movie '{movie_title}' already exists in the database.")
                return

            connection.execute(
                text(
                    "INSERT INTO movies (title, year, rating, poster) "
                    "VALUES (:title, :year, :rating, :poster)"
                ),
                {"title": movie_title, "year": year, "rating": rating, "poster": poster}
            )

        print(f"Movie '{movie_title}' added successfully!")
        print(f"Year: {year}, Rating: {rating}")
        print(f"Poster URL: {poster}")

    except requests.exceptions.RequestException as e:
        print(f"Network error while fetching movie '{title}': {e}")
    except Exception as e:
        print(f"Error adding movie '{title}': {e}")


def delete_movie(title):
    """Delete a movie from the database (case-insensitive)."""
    with engine.begin() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE lower(title) = lower(:title)"),
            {"title": title}
        )

        if result.rowcount > 0:
            print(f"Movie '{title}' deleted successfully.")
        else:
            print(f"Movie '{title}' not found.")


def update_movie(title, rating):
    """Update a movie's rating in the database (case-insensitive)."""
    with engine.begin() as connection:
        result = connection.execute(
            text("UPDATE movies SET rating = :rating WHERE lower(title) = lower(:title)"),
            {"title": title, "rating": rating}
        )

        if result.rowcount > 0:
            print(f"Movie '{title}' rating updated to {rating}.")
        else:
            print(f"Movie '{title}' not found.")

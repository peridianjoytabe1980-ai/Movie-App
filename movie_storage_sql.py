from sqlalchemy import create_engine, text
import requests


engine = create_engine("sqlite:///movies.db")

with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS movies"))
    connection.execute(text("""
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER,
            rating REAL,
            poster TEXT
        )
    """))
    connection.commit()

# ---------------------------
# FUNCTIONS
# ---------------------------

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
        # Fetch movie data from OMDb
        response = requests.get(OMDB_URL, params={"t": title, "apikey": "621a1d46"})
        response.raise_for_status()
        data = response.json()

        # Check if movie exists
        if data.get("Response") == "False":
            print(f"Movie '{title}' not found.")
            return

        # Extract fields
        movie_title = data.get("Title")
        year = data.get("Year")
        rating = data.get("imdbRating")
        poster = data.get("Poster")

        # Insert into DB
        with engine.connect() as connection:
            connection.execute(
                text("INSERT INTO movies (title, year, rating, poster) VALUES (:title, :year, :rating, :poster)"),
                {"title": movie_title, "year": year, "rating": rating, "poster": poster}
            )
            connection.commit()

        print(f"Movie '{movie_title}' added successfully.")
        print(f"Year: {year}, Rating: {rating}")
        print(f"Poster: {poster}")

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Error adding movie: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(
                text("DELETE FROM movies WHERE title = :title"), {"title": title}
            )
            connection.commit()
            if result.rowcount > 0:
                print(f"Movie '{title}' deleted successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error deleting movie: {e}")


def update_movie(title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            result = connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"title": title, "rating": rating}
            )
            connection.commit()
            if result.rowcount > 0:
                print(f"Movie '{title}' rating updated to {rating}.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error updating movie: {e}")

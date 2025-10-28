import json
import os

FILE_NAME = "../data.json"


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """

    def get_movies():
        """Load movies from data.json and return them as a dictionary."""

    if not os.path.exists(FILE_NAME):
        # File missing → return empty dict
        return {}

    try:
        with open(FILE_NAME, "r") as f:
            content = f.read().strip()
            if not content:  # empty file
                return {}
            movies = json.loads(content)
            return movies
    except json.JSONDecodeError:
        # File corrupt → return empty dict
        return {}


def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open(FILE_NAME, "w") as f:
        json.dump(movies, f, indent=4)


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title] = {"year": year, "rating": rating}
    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    if title in movies:
        del movies[title]
        save_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    if title in movies:
        movies[title]["rating"] = rating
        save_movies(movies)

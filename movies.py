import statistics
import random
import requests
from storage import movie_storage_sql as storage
from storage import movie_storage  # JSON storage, only for migration

# -----------------------------
# OMDb API config
# -----------------------------
OMDB_API_KEY = "621a1d46"
OMDB_URL = "https://www.omdbapi.com/"

def get_poster(title):
    """Fetch poster URL from OMDb API for a given movie title."""
    try:
        response = requests.get(OMDB_URL, params={"t": title, "apikey": OMDB_API_KEY})
        data = response.json()
        if data.get("Response") == "True":
            return data.get("Poster", "")
    except:
        pass
    return ""

# -----------------------------
# Migration from JSON to SQL
# -----------------------------

def migrate_json_to_sql():
    """Migrate movies from JSON to SQL if not already present or missing poster."""
    sql_movies = storage.list_movies()
    json_movies = movie_storage.get_movies()

    with storage.engine.begin() as conn:
        for title, info in json_movies.items():
            poster = get_poster(title)
            if title not in sql_movies:
                # Insert new movie
                conn.execute(
                    storage.text("""
                        INSERT INTO movies (title, year, rating, poster)
                        VALUES (:title, :year, :rating, :poster)
                    """),
                    {"title": title, "year": info.get("year"), "rating": info.get("rating"), "poster": poster}
                )
            else:
                # Update poster if missing
                existing = sql_movies[title]
                if not existing.get("poster") and poster:
                    conn.execute(
                        storage.text("""
                            UPDATE movies
                            SET poster = :poster
                            WHERE title = :title
                        """),
                        {"poster": poster, "title": title}
                    )


# -----------------------------
# Menu and functions
# -----------------------------
def show_menu():
    print("\n" + "*" * 10, "My Movies Database", "*" * 10)
    menu = {
        0: "Exit",
        1: "List movies",
        2: "Add movie",
        3: "Delete movie",
        4: "Update movie",
        5: "Stats",
        6: "Random movie",
        7: "Search movie",
        8: "Movies sorted by rating",
        9: "Generate website",
    }
    for number, name in menu.items():
        print(f"{number}. {name}")
    return menu

def list_movies():
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")

def add_movie_menu():
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    storage.add_movie(title)

def delete_movie():
    movies = storage.list_movies()
    title = input("Enter movie title: ").strip()
    title_map = {t.lower(): t for t in movies.keys()}
    lower_title = title.lower()
    if lower_title in title_map:
        actual_title = title_map[lower_title]
        storage.delete_movie(actual_title)
        print(f"{actual_title} has been deleted successfully.")
        list_movies()
    else:
        print("That movie does not exist.")

def update_movie():
    movies = storage.list_movies()
    title = input("Enter movie title: ").strip()
    title_map = {t.lower(): t for t in movies.keys()}
    lower_title = title.lower()
    if lower_title not in title_map:
        print("That movie does not exist.")
        return
    actual_title = title_map[lower_title]
    try:
        rating = float(input("Enter new movie rating (1-10): "))
        if not (1 <= rating <= 10):
            print("Rating must be between 1 and 10.")
            return
    except ValueError:
        print("Invalid rating input.")
        return
    storage.update_movie(actual_title, rating)
    print(f"{actual_title} has been updated successfully.")
    list_movies()

def stats():
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return
    ratings = [info["rating"] for info in movies.values() if info["rating"] and info["rating"] != "N/A"]
    ratings = [float(r) for r in ratings]
    if not ratings:
        print("No valid ratings available.")
        return
    average = statistics.mean(ratings)
    median = statistics.median(ratings)
    best_rating = max(ratings)
    worst_rating = min(ratings)
    best_movies = [title for title, info in movies.items() if float(info["rating"]) == best_rating]
    worst_movies = [title for title, info in movies.items() if float(info["rating"]) == worst_rating]
    print(f"The average rating is: {average:.2f}")
    print(f"The median rating is: {median:.2f}")
    print(f"The best movie(s): {', '.join(best_movies)} ({best_rating})")
    print(f"The worst movie(s): {', '.join(worst_movies)} ({worst_rating})")

def random_movie():
    movies = storage.list_movies()
    if not movies:
        print("No movies available.")
        return
    title, info = random.choice(list(movies.items()))
    print(f"Random movie suggestion: {title} ({info['year']}) with rating {info['rating']}")

def search_movie():
    movies = storage.list_movies()
    search = input("Enter part of the movie name: ").strip().lower()
    found = [f"{title} ({info['year']}): {info['rating']}" for title, info in movies.items() if search in title.lower()]
    if found:
        print("\n".join(found))
    else:
        print("No matching movies found.")

def sorted_movies():
    movies = storage.list_movies()
    sorted_list = sorted(
        movies.items(),
        key=lambda x: float(x[1]["rating"]) if x[1]["rating"] and x[1]["rating"] != "N/A" else 0,
        reverse=True
    )
    for title, info in sorted_list:
        print(f"{title} ({info['year']}): {info['rating']}")

def generate_website():
    movies = storage.list_movies()
    with open("_static/index_template.html", "r", encoding="utf-8") as f:
        template = f.read()
    movie_grid = ""
    for title, info in movies.items():
        poster = info.get("poster", "")
        year = info.get("year", "")
        rating = info.get("rating", "")
        movie_grid += f"""
        <li class="movie-item">
            <img src="{poster}" alt="{title} poster"/>
            <h3>{title}</h3>
            <p>Year: {year}</p>
            <p>Rating: {rating}</p>
        </li>
        """
    html_content = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)
    with open("_static/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Website was generated successfully.")

# -----------------------------
# Main
# -----------------------------
def main():
    migrate_json_to_sql()  # Auto-migrate old movies with posters

    while True:
        menu = show_menu()
        choice = input("Enter choice (0-9): ").strip()
        if not choice.isdigit() or int(choice) not in menu:
            print("Invalid choice")
            continue
        choice = int(choice)
        if choice == 0:
            print("Bye!")
            break
        elif choice == 1:
            list_movies()
        elif choice == 2:
            add_movie_menu()
        elif choice == 3:
            delete_movie()
        elif choice == 4:
            update_movie()
        elif choice == 5:
            stats()
        elif choice == 6:
            random_movie()
        elif choice == 7:
            search_movie()
        elif choice == 8:
            sorted_movies()
        elif choice == 9:
            generate_website()

if __name__ == "__main__":
    main()

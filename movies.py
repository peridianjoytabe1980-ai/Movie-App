import statistics
import random
import movie_storage
import movie_storage_sql as storage

def command_list_movies():
    """Retrieve and display all movies from the database."""
    movies = storage.list_movies()
    print(f"{len(movies)} movies in total")
    for movie, data in movies.items():
        print(f"{movie} ({data['year']}): {data['rating']}")


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
    movies = movie_storage.get_movies()
    print(f"{len(movies)} movies in total")
    for title, info in movies.items():
        print(f"{title} ({info['year']}): {info['rating']}")


def add_movie_menu():
    """Add a movie using OMDb API (fetches year, rating, poster automatically)."""
    title = input("Enter movie title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return

    # Call the OMDb-powered storage function
    from movie_storage_sql import add_movie  # make sure this points to your updated storage file
    add_movie(title)



def delete_movie():
    movies = movie_storage.get_movies()
    title = input("Enter movie title: ").strip()
    if title in movies:
        movie_storage.delete_movie(title)
        print(f"{title} has been deleted successfully")
        list_movies()
    else:
        print("That movie does not exist")


def update_movie():
    movies = movie_storage.get_movies()
    title = input("Enter movie title: ").strip()
    if title not in movies:
        print("That movie does not exist")
        return

    try:
        rating = float(input("Enter new movie rating (1-10): "))
        if not (1 <= rating <= 10):
            print("Rating must be between 1 and 10.")
            return
    except ValueError:
        print("Invalid rating input.")
        return

    movie_storage.update_movie(title, rating)
    print(f"{title} has been updated successfully")
    list_movies()


def stats():
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies available.")
        return

    ratings = [info["rating"] for info in movies.values()]
    average = statistics.mean(ratings)
    median = statistics.median(ratings)
    best_rating = max(ratings)
    worst_rating = min(ratings)

    best_movies = [title for title, info in movies.items() if info["rating"] == best_rating]
    worst_movies = [title for title, info in movies.items() if info["rating"] == worst_rating]

    print(f"The average rating is: {average:.2f}")
    print(f"The median rating is: {median:.2f}")
    print(f"The best movie(s): {', '.join(best_movies)} ({best_rating})")
    print(f"The worst movie(s): {', '.join(worst_movies)} ({worst_rating})")


def random_movie():
    movies = movie_storage.get_movies()
    if not movies:
        print("No movies available.")
        return
    title, info = random.choice(list(movies.items()))
    print(f"Random movie suggestion: {title} ({info['year']}) with rating {info['rating']}")


def search_movie():
    movies = movie_storage.get_movies()
    search = input("Enter part of the movie name: ").strip().lower()
    found = [f"{title} ({info['year']}): {info['rating']}"
             for title, info in movies.items() if search in title.lower()]
    if found:
        print("\n".join(found))
    else:
        print("No matching movies found.")


def sorted_movies():
    movies = movie_storage.get_movies()
    sorted_list = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
    for title, info in sorted_list:
        print(f"{title} ({info['year']}): {info['rating']}")


def generate_website():
    from movie_storage_sql import list_movies  # import your database function

    movies = list_movies()  # get all movies

    # Load your template
    with open("_static/index_template.html", "r", encoding="utf-8") as f:
        template = f.read()

    # Generate movie grid HTML
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

    # Replace the placeholder in the template
    html_content = template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    # Write to the output file
    with open("_static/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("Website was generated successfully.")



def main():
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

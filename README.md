A Python-based command-line application for managing a personal movie database.
The project enables users to add, update, delete, search, and analyze movies, while also integrating external movie data from the OMDb API.
It includes database migration from JSON → SQL, and can generate a static website showcasing all stored movies.

📌 Core Functionality
Add new movies
Delete movies
Update movie ratings
Search movies by keyword
Display sorted movies (by rating)
View statistics: average, median, best & worst movies
Get a random movie suggestion

🌐 API Integration
Uses the OMDb API to automatically fetch:
Movie posters
Additional metadata (title, year, etc.)

🗄️ Database Support
Reads existing movie data from JSON
Migrates data into an SQL database using SQLite + SQLAlchemy
Automatically updates missing poster URLs

🌍 Website Generation
Generates a static HTML page displaying all movies with:
Posters, Titles, Year, Ratings

🛠️ Technologies Used
Python
Requests (API calls)
SQLAlchemy & SQLite
OMDb API
HTML & CSS (for the generated website)
Statistics (for rating calculations)

Git/GitHub

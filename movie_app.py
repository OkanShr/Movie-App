import random
import requests
from istorage import IStorage

# This is the API key you got from OMDb, but it doesn't work
OMDB_API_KEY = '853b022f'


class MovieApp:
    """
    A class representing a movie database application.

    Attributes:
        _storage (IStorage): An object implementing the IStorage interface
        for data storage.
    """

    def __init__(self, storage: IStorage):
        """
        Initializes the MovieApp with a storage object.

        Args:
            storage (IStorage): An object implementing the IStorage interface.
        """
        self._storage = storage

    def _command_add_movie(self):
        """
        Command to add a movie to the database.
        Fetches movie data from OMDb API based on user input and saves
        it to storage.
        """
        title = input("Enter new movie name: ")
        movie_data = self._fetch_movie_data(title)
        if movie_data:
            self._storage.add_movie(movie_data["Title"],
                                    movie_data["Year"],
                                    movie_data["imdbRating"],
                                    movie_data["Poster"])
            print(f"Movie {title} successfully added")
        else:
            print(f"Movie {title} could not be found or there was "
                  f"an error fetching the data.")

    @staticmethod
    def _fetch_movie_data(title):
        """
        Fetches movie data from OMDb API.

        Args:
            title (str): The title of the movie to fetch.

        Returns:
            dict: Movie data as returned by OMDb API.
                  None if movie is not found or an error occurs.
        """
        try:
            response = requests.get(f"http://www.omdbapi.com/?"
                                    f"apikey={OMDB_API_KEY}&"
                                    f"t={title}")
            if response.status_code == 200:
                data = response.json()
                if data['Response'] == 'True':
                    return data
                else:
                    print(f"Error: {data['Error']}")
            else:
                print("Error: Could not retrieve data from OMDb API.")
        except requests.RequestException as e:
            print(f"Error: {e}")
        return None

    def _command_delete_movie(self):
        """
        Command to delete a movie from the database.
        """
        title = input("Enter movie name to delete: ")
        self._storage.delete_movie(title)
        print(f"Movie {title} deleted.")

    def _command_update_movie(self):
        """
        Command to update a movie's information in the database.
        """
        title = input("Enter movie name to update: ")
        year = int(input("Enter new year of release: "))
        rating = float(input("Enter new rating (1-10): "))
        self._storage.update_movie(title, year, rating)
        print(f"Movie {title} updated.")

    def _command_list_movies(self):
        """
        Command to list all movies in the database.
        """
        movies = self._storage.list_movies()
        print(f"{len(movies)} movies in total")
        for title, details in movies.items():
            print(f"{title} ({details['year']}): {details['rating']}")

    def _command_movie_stats(self):
        """
        Command to print statistics about the movies in the database:
        - Average rating
        - Median rating
        - Best and worst movies by rating
        """
        try:
            movies = self._storage.list_movies()
            ratings = [float(details['rating']) for details in movies.values()]

            avg_rating = sum(ratings) / len(ratings)
            print(f"Average rating: {avg_rating:.1f}")

            sorted_ratings = sorted(ratings)
            mid = len(sorted_ratings) // 2
            if len(sorted_ratings) % 2 == 0:
                median_rating = (sorted_ratings[mid - 1] +
                                 sorted_ratings[mid]) / 2
            else:
                median_rating = sorted_ratings[mid]
            print(f"Median rating: {median_rating:.1f}")

            best_rating = max(ratings)
            best_movies = [title for title, details in movies.items()
                           if details['rating'] == str(best_rating)]
            print("Best movie(s) by rating:")
            for movie in best_movies:
                print(f"{movie} ({best_rating})")

            worst_rating = min(ratings)
            worst_movies = [title for title, details in movies.items()
                            if details['rating'] == str(worst_rating)]
            print("Worst movie(s) by rating:")
            for movie in worst_movies:
                print(f"{movie} ({worst_rating})")
        except ValueError as error:
            print("An error occurred:", error)

    def _command_random_movie(self):
        """
        Command to print a random movie from the database.
        """
        try:
            movies = self._storage.list_movies()
            if movies:
                title, details = random.choice(list(movies.items()))
                print(f"Random movie: {title} ({details['year']}), "
                      f"{details['rating']}")
            else:
                print("No movies in the database.")
        except ValueError as error:
            print("An error occurred:", error)

    def _command_search_movie(self):
        """
        Command to search for movies in the database based on a query.
        """
        try:
            query = input("Enter part of movie name: ").lower()
            movies = self._storage.list_movies()
            matches = [(title, details['rating']) for title, details in
                       movies.items() if query in title.lower()]
            print("Movies matching the query:")
            for match in matches:
                print(f"{match[0]}, {match[1]}")
        except ValueError as error:
            print("An error occurred:", error)

    def _command_print_sorted_movies_by_rating(self):
        """
        Command to print all movies in the database sorted by rating.
        """
        try:
            movies = self._storage.list_movies()
            sorted_movies = sorted(movies.items(),
                                   key=lambda x: x[1]['rating'], reverse=True)
            print("Movies sorted by rating:")
            for title, details in sorted_movies:
                print(f"{title}, {details['rating']}")
        except ValueError as error:
            print("An error occurred:", error)

    def _command_print_sorted_movies_by_year(self):
        """
        Command to print all movies in the database sorted by year.(Newest
        First)
        """
        try:
            movies = self._storage.list_movies()
            sorted_movies = sorted(movies.items(), key=lambda x: x[1]['year'],
                                   reverse=True)
            print("Movies sorted by year:")
            for title, details in sorted_movies:
                print(f"{title} ({details['year']}), {details['rating']}")
        except ValueError as error:
            print("An error occurred:", error)
        except Exception as e:
            print("An unexpected error occurred:", e)

    def _command_filter_movies(self):
        """
        Command to filter movies in the database based on minimum rating,
        start year, and end year.
        """
        try:
            min_rating_input = input("Enter minimum rating "
                                     "(leave blank for no minimum rating): ")
            start_year_input = input("Enter start year "
                                     "(leave blank for no start year): ")
            end_year_input = input("Enter end year "
                                   "(leave blank for no end year): ")

            min_rating = float(min_rating_input) if min_rating_input else None
            start_year = int(start_year_input) if start_year_input else None
            end_year = int(end_year_input) if end_year_input else None

            movies = self._storage.list_movies()

            filtered_movies = {}
            for title, details in movies.items():
                if (min_rating is None or float(details['rating']) >=
                    min_rating) and (start_year is None or
                                     float(details['year']) >= start_year) \
                        and (end_year is None or float(details['year']) <=
                             end_year):
                    filtered_movies[title] = details
            if len(filtered_movies) > 0:
                print("\nFiltered Movies:")
                for title, details in filtered_movies.items():
                    print(f"{title} ({details['year']}), "
                          f"Rating: {details['rating']}")

                return filtered_movies
            else:
                print("No movies found for this filter")
        except ValueError:
            print("Invalid input. Please enter valid numbers for "
                  "rating and years.")
            return []

    def _generate_website(self):
        """
        Generates a website based on the movies in the database.
        """
        try:
            with open("./_static/index_template.html",
                      "r") as template_file_obj:
                template_file = template_file_obj.read()
        except FileNotFoundError as e:
            print("Template file not found:", e)
            return
        except Exception as e:
            print("An error occurred while reading the template file:", e)
            return

        try:
            movie_grid = self._generate_movies_grid()
            with open("index.html", "w") as new_file_obj:
                new_file_obj.write(
                    template_file.replace("__TEMPLATE_MOVIE_GRID__",
                                          movie_grid))
            print("Website Generated Successfully")
        except Exception as e:
            print("An error occurred while writing the new file:", e)

    def _generate_movies_grid(self):
        movies = self._storage.list_movies()
        movie_grid = ""
        for title, details in movies.items():
            movie_grid += (
                "<div class='movie'>\n"
                f"<img src='{details['poster']}' alt='{title} poster' "
                f"class='movie-poster'>\n"
                f"<li class='movie-title'>{title}</li>\n"
                f"<li class='movie-year'>{details['year']}</li>\n"
                "</div>\n"
            )
        return movie_grid

    def run(self):
        """
        Main method to run the MovieApp and display the CLI menu.
        """
        print("********** My Movies Database **********")

        while True:
            print("\nMenu:")
            print("0. Exit")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Update Movie")
            print("5. Stats")
            print("6. Random Movie")
            print("7. Search Movie")
            print("8. Movies sorted by rating")
            print("9. Movies sorted by year")
            print("10. Filter Movies")
            print("11. Generate Website")
            choice = input("Enter your choice: ")

            try:
                choice = int(choice)
                if choice == 0:
                    print("Exiting...")
                    break
                elif choice == 1:
                    self._command_list_movies()
                elif choice == 2:
                    self._command_add_movie()
                elif choice == 3:
                    self._command_delete_movie()
                elif choice == 4:
                    self._command_update_movie()
                elif choice == 5:
                    self._command_movie_stats()
                elif choice == 6:
                    self._command_random_movie()
                elif choice == 7:
                    self._command_search_movie()
                elif choice == 8:
                    self._command_print_sorted_movies_by_rating()
                elif choice == 9:
                    self._command_print_sorted_movies_by_year()
                elif choice == 10:
                    self._command_filter_movies()
                elif choice == 11:
                    self._generate_website()
                else:
                    print("Invalid choice. Please enter a number "
                          "between 0 and 10.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            _continue = input("\nContinue..")

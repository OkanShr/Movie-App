from storage_json import StorageJson
from movie_app import MovieApp

# Should I define this inside main or outside it?
# normally I would put it in a .env file
MOVIE_DATA_FILE = "data.json"


def main():
    """
    Main function of project
    """
    storage = StorageJson(MOVIE_DATA_FILE)

    app = MovieApp(storage)
    # Running the app
    app.run()


if __name__ == "__main__":
    main()

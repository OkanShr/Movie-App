from storage.storage_csv import StorageCsv
from movie_app import MovieApp

# Should I define this inside main or outside it?
# normally I would put it in a .env file
MOVIE_DATA_FILE_JSON = "data/data.json"
MOVIE_DATA_FILE_CSV = "data/data.csv"


def main():
    """
    Main function of project
    """
    storage = StorageCsv(MOVIE_DATA_FILE_CSV)

    app = MovieApp(storage)
    # Running the app
    app.run()


if __name__ == "__main__":
    main()

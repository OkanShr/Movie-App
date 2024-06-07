import json
from istorage import IStorage

MOVIE_DATA_FILE = "data.json"


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """
        Loads movie data from the JSON file.
        If the file doesn't exist or is empty, returns an empty dictionary.
        """
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        return data

    def save_data(self, data):
        """
        Saves movie data to the JSON file.
        """
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def list_movies(self):
        """
        Returns a dictionary of all movies.
        """
        return self.load_data()

    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the movie dictionary.
        """
        data = self.load_data()
        data[title] = {"year": year, "rating": rating, "poster": poster}
        self.save_data(data)

    def delete_movie(self, title):
        """
        Deletes a movie from the movie dictionary by its title.
        """
        data = self.load_data()
        if title in data:
            del data[title]
            self.save_data(data)

    def update_movie(self, title, year, rating):
        """
        Updates the information of a movie in the movie dictionary.
        """
        data = self.load_data()
        if title in data:
            data[title]["year"] = year
            data[title]["rating"] = rating
            self.save_data(data)


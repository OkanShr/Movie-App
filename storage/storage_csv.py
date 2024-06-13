import csv
import json

from storage.istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def check_if_exists(self, title):
        """
        Checks if the Movie name exists in the database.

        :param title: Title of the movie to check.
        :return: True if the movie exists, False otherwise.
        """
        movies = self.load_data()
        return title in movies

    def load_data(self):
        """
        Loads movie data from the CSV file.
        If the file doesn't exist or is empty, returns an empty dictionary.

        :return: A dictionary with movie titles as keys and movie
        details as values.
        """
        movies = {}
        try:
            with open(self.file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        title = row['title']
                        movies[title] = {
                            'year': int(row['year']),
                            'rating': float(row['rating']),
                            'poster': row['poster']
                        }
                    except KeyError as e:
                        print(
                            f"Missing expected column in row: {row}. "
                            f"Error: {e}")
                    except ValueError as e:
                        print(
                            f"Error converting data types in row: {row}. "
                            f"Error: {e}")
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
        except csv.Error as e:
            print(f"Error reading CSV file {self.file_path}: {e}")
        return movies

    def save_data(self, data):
        """
        Saves movie data to the CSV file.
        """
        try:
            with open(self.file_path, mode='w', newline='') as file:
                fieldnames = ['title', 'year', 'rating', 'poster']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for title, info in data.items():
                    writer.writerow({
                        'title': title,
                        'year': info['year'],
                        'rating': info['rating'],
                        'poster': info['poster']
                    })
        except csv.Error as e:
            print(f"Error saving data to {self.file_path}: {e}")

    def list_movies(self):
        """
        Returns a dictionary of all movies.
        """
        return self.load_data()

    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the movie dictionary and saves to the CSV file.
        """
        data = self.load_data()
        data[title] = {"year": year, "rating": rating, "poster": poster}
        self.save_data(data)

    def delete_movie(self, title):
        """
        Deletes a movie from the movie dictionary and saves to the CSV file.
        """
        data = self.load_data()
        if title in data:
            del data[title]
            self.save_data(data)

    def update_movie(self, title, year, rating):
        """
        Updates the information of a movie in the movie dictionary
        and saves to the CSV file.
        """
        data = self.load_data()
        if title in data:
            data[title]["year"] = year
            data[title]["rating"] = rating
            self.save_data(data)
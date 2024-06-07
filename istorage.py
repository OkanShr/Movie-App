from abc import ABC, abstractmethod

MOVIE_DATA_FILE = "data.json"


class IStorage(ABC):
    """
    CRUD Interface for StorageJson
    """
    @abstractmethod
    def list_movies(self):
        """
        Method to fetch Movies
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Method to add Movie
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Method to delete Movie
        """
        pass

    @abstractmethod
    def update_movie(self, title, year, rating):
        """
        Method to update Movie
        """
        pass

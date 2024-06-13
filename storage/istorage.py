from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    CRUD Interface for StorageJson
    """
    @abstractmethod
    def check_if_exists(self, title):
        """
        Method to check if Movie exists in db
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

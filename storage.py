import json
from abc import ABC, abstractmethod
from uuid import uuid4
from pathlib import Path
import pymongo
import config


class BaseStorage(ABC):

    @abstractmethod
    def create_film(self, film: dict):
        pass

    @abstractmethod
    def get_film(self, film_id):
        pass

    @abstractmethod
    def get_film_by_name(self, *, search_param: str = None, skip: int, limit: int):
        pass

    @abstractmethod
    def get_content(self, page_limit: int, page: int):
        pass

    @abstractmethod
    def rate_film(self, film_id: str, like_it: bool):
        pass

    @abstractmethod
    def delete_film(self, film_id: str):
        pass


class JSONStorage(BaseStorage):

    def __init__(self, file_name: str = "Storage.json"):

        self.file_name = file_name

        my_file = Path(self.file_name)

        if not my_file.is_file():

            with open(self.file_name, mode='w', encoding='utf-8') as file:

                json.dump([], file, indent=4)

    def create_film(self, film: dict):

        film['uuid'] = str(uuid4())

        with open(self.file_name, mode='r') as file:

            content: list[dict] = json.load(file)

        content.append(film)

        with open(self.file_name, mode='w', encoding='utf-8') as file:

            json.dump(content, file, indent=4)

        return film

    def get_film(self, film_id):
        pass

    def get_film_by_name(self, skip: int = 0, limit: int = 10, search_param: str = None) -> list[dict]:

        with open(self.file_name, mode='r') as file:

            content: list[dict] = json.load(file)

            result = []

            if not search_param:

                result = content

                return result

            for film in content:

                if search_param in film["title"]:

                    result.append(film)

            return result

    def get_content(self, page_limit: int, page: int):
        pass

    def rate_film(self, film_id: str, like_it: bool):

        with open(self.file_name, mode='r') as file:

            content: list[dict] = json.load(file)

        for film in content:

            if film["uuid"] == film_id:

                film_rating = film["rating"]
                already_liked_it = (film_rating * film["votes"]) / 100

                if like_it:
                    already_liked_it += 1

                film_votes = film["votes"] + 1
                new_rating = round((already_liked_it / film_votes) * 100, 2)

                film["rating"] = new_rating
                film["votes"] = film_votes

                break

        with open(self.file_name, mode='w', encoding='utf-8') as file:

            json.dump(content, file, indent=4)

    def delete_film(self, film_id: str):

        with open(self.file_name, mode='r') as file:

            content: list[dict] = json.load(file)

        for film in content:

            if film["uuid"] == film_id:

                content.remove(film)

                break

        with open(self.file_name, mode='w', encoding='utf-8') as file:

            json.dump(content, file, indent=4)


class MongoStorage(BaseStorage):

    def __init__(self):

        url = ('mongodb+srv://{user}:{password}@cluster0.ieqgldq.mongodb.net/?retryWrites=true&w=majority'
               .format(user=config.USER, password=config.PASSWORD))

        client = pymongo.MongoClient(url)
        db = client['movies']

        self.movies_collection = db['movies_collection']

    def create_film(self, film: dict):

        film['uuid'] = str(uuid4())

        self.movies_collection.insert_one(film)

        return film

    def get_film_by_name(self, *, search_param: str = None, skip: int, limit: int):

        query = {}

        detected_films = []

        if search_param:

            query = {"title": {"$regex": search_param.strip()}}

        films = self.movies_collection.find(query).sort('rating', -1).skip(skip).limit(limit)

        for film in films:

            del film['_id']
            detected_films.append(film)

        return detected_films

    def get_film(self, film_id):

        query = {"uuid": film_id}

        film = self.movies_collection.find_one(query)

        return film

    def get_content(self, page_limit: int, page: int):

        skip = (page - 1) * page_limit

        content = self.movies_collection.find().skip(skip).limit(page_limit)

        movies = []

        for movie in content:

            del movie['_id']
            movies.append(movie)

        return movies

    def get_films_by_genre(self, genre: str, page_limit: int = 10, page: int = 1):

        query = {"genres": genre}

        skip = (page - 1) * page_limit

        content = self.movies_collection.find(query).skip(skip).limit(page_limit)

        movies = []

        for movie in content:

            del movie['_id']
            movies.append(movie)

        return movies

    def rate_film(self, film_id: str, like_it: bool):

        film = self.get_film(film_id=film_id)

        film_rating = film["rating"]
        already_liked_it = (film_rating * film["votes"]) / 100

        if like_it:

            already_liked_it += 1

        film_votes = film["votes"] + 1
        new_rating = round((already_liked_it/film_votes) * 100, 2)

        rated_movie = self.movies_collection.update_one({"uuid": film_id},
                                                        {'$set': {"rating": new_rating, "votes": film_votes}})

        return rated_movie

    def delete_film(self, film_id: str):

        self.movies_collection.delete_one({"uuid": film_id})

        return None


storage = MongoStorage()

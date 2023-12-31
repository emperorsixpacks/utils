import string
import unicodedata
from bson import ObjectId
from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder
from dataclasses import dataclass, field
from typing import List
import math
import numpy as np


def character_decode(input_string):
    nfkd_form = unicodedata.normalize("NFKD", input_string)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def remove_punctuation_except_hyphen(input_string):
    translator = str.maketrans('', '', string.punctuation.replace('-', ''))
    cleaned_string = input_string.translate(translator)
    return cleaned_string


class PyObjectID(ObjectId):
    # We convert the _ID to a string before storing it

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.upper(type="string")


class Movie(BaseModel):
    id: PyObjectID = Field(default_factory=PyObjectID, alias="_id")
    title: str = Field(default=None)
    slug: str = Field(default=None)
    original_title: str = Field(default=None)
    genres: list = Field(default=None)
    cast: list = Field(default=None)
    crew: list = Field(default=None)
    tmdb_id: int = Field(default=None)
    imdb_id: str = Field(default=None)
    overview: str = Field(default=None)
    summary: str = Field(default=None)
    reviews: list = Field(default=None)
    popularity: float = Field(default=None)
    runtime: int = Field(default=None)
    movie_location: str = Field(default=None)
    where_to_watch: list = Field(default=None)
    sentiment: list = Field(default=None)
    release_date: str = Field(default=None)
    original_language: str = Field(default=None)
    poster_path: str = Field(default=None)

    class Config:
        populate_by_name = True
        from_attributes = True
        json_encoders = {ObjectId: str}

    def save(self, database) -> bool:
        if database.insert_one(jsonable_encoder(self)):
            return True
        return False



class Title:

    def __init__(self, movie_title: str):
        self.title = movie_title
        self.slug = self.title.lower().replace(" ", "-")
        self.original_title = movie_title.strip().title()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        _filtered_title = character_decode(value.strip().title())
        self._title = remove_punctuation_except_hyphen(_filtered_title)



def getMoviefromDB(title: Title, tmdb_id, database):
    query = {"title": title.title, "tmdb_id": tmdb_id}

    movies = database.find(query)
    if movies:
        for movie in movies:
            for key, value in movie.items():
                if hasattr(Movie, key):
                    setattr(Movie, key, value)
            return Movie
    return None



@dataclass()
class MovieDetail:
    id: str = field(default=None)
    title: str = field(default=None)
    sentiment: list = field(default=None)
    overview: str = Field(default=None)
    genres: list = field(default=None)
    cast: list = field(default=None)
    crew: list = field(default=None)
    tmdb_id: int = field(default=None)
    imdb_id: str = field(default=None)
    popularity: float = field(default=None)
    poster_path: str = field(default=None)
    where_to_watch: list = field(default=None)
    original_title: str = field(default=None)
    original_language: str = field(default=None)
    runtime: int = field(default=None)
    release_date: str = field(default=None)
    summary: str = field(default=None)
    



@dataclass
class Where_to_watch:
    service: str = field(default=None)
    link: str = field(default=None)

@dataclass
class Scrapper:
    where_to_watch: List[Where_to_watch] = field(default=None)
    reviews: list = field(default=None)

@dataclass
class Result:
    id: str = field(default=None)
    title: str = field(default=None)
    popularity: float = field(default=None)
    overview: str = field(default=None)
    release_date: str = field(default=None)

@dataclass
class SearchResult:
    results: List[Result]
    total_results: int

    def __init__(self, result: List[dict]):
        movies_list = []
        popularity_scores = []
        for movie_search in result:
            movie = MovieDetail(**{field:value for field, value in movie_search.items() if field in vars(MovieDetail)})
            movies_list.append(movie)
            popularity_scores.append(movie.popularity)

        average_popularity_score = np.mean(popularity_scores)

        # Filter movies by popularity score and assign to self.result
        self.results = [Result(**{field: value for field, value in vars(movie).items() if field in vars(Result)}) for movie in movies_list if movie.popularity >= average_popularity_score]
        self.total_results = len(self.results)



@dataclass(init=False)
class Credits:
    name: str = field(default=None)
    character: str = field(default=None)
    original_name: str = field(default=None)
    known_for_department: str = field(default=None)

    def __call__(self, *args, **kwargs):
        pass


def return_credits(result: dict)->list:
    cast_list = []
    crew_list = []
    credit = {
            "name":str,
            "character": str,
            "original_name": str,
            "known_for_department": str,
        }
    cast_list  = [{key:value for key, value in cast.items() if key in credit} for cast in result["cast"]]
    crew_list  = [{key:value for key, value in cast.items() if key in credit} for cast in result["crew"]]
    
    return cast_list, crew_list




if __name__ == "__main__":
    print(hasattr(Result, "id"))
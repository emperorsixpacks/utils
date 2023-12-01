import os
import math
import json
import requests
try:
    from .models import MovieDetail, SearchResult, return_credits
except ImportError:
    from models import MovieDetail, SearchResult, return_credits


class TMDBWrapper:

    def __init__(self, api_key):
        self.api_key = api_key

    def search(self, query: str, **kwargs):

        query = query
        if kwargs.get('year'):
            param = f"search/movie?query={query}&primary_release_year={kwargs.get('year')}"
        else:
            param = f"search/movie?query={query}"
        search_result = self._get(param)
        if search_result:
            movies_result = search_result["results"]

            if search_result["total_results"] == 0:
                return False
            return SearchResult(result=movies_result)
        return None

    def get_trending_today(self):
        param = "trending/movie/day?language=en-US"
        search_result = self._get(param)
        movies_result = search_result["results"]
        return SearchResult(result=movies_result)

    def get_trending_week(self):
        param = "trending/movie/week?language=en-US"
        search_result = self._get(param)
        movies_result = search_result["results"]
        return SearchResult(result=movies_result)

    def get_movie(self, tmdb_id: int):
        param = f"movie/{tmdb_id}?language=en-US"
        result = self._get(param)
        cast, crew = self.get_credits(tmdb_id=tmdb_id)
        movie = MovieDetail(**{field:value for field, value in result.items() if field in vars(MovieDetail)})
        movie.cast = cast
        movie.crew = crew
        movie.tmdb_id = result["id"]
        return movie

    def get_credits(self, tmdb_id:int):
        param = f"/movie/{tmdb_id}/credits?language=en-US"
        result = self._get(param)
        return return_credits(result)

    def _get(self, params):
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        url = f"https://api.themoviedb.org/3/{params}"
        response = requests.get(url=url, headers=headers)
        if response:
            return json.loads(response.text)
        return False


if __name__ == "__main__":
    import os
    API_KEY = os.getenv("API_KEY")
    tmdb = TMDBWrapper(api_key=API_KEY)
    print(tmdb.search(query="barbie"))
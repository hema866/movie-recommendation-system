import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

API_KEY = "9be2139eb7649fcf61b7477464a8269c"

# Store previously fetched posters
poster_cache = {}

# Create a session with automatic retries
session = requests.Session()

retry_strategy = Retry(
    total=3,
    connect=3,
    read=2,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)


def fetch_poster(movie_name):

    if not movie_name:
        return "https://placehold.co/300x450?text=No+Poster"

    if movie_name in poster_cache:
        return poster_cache[movie_name]

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": movie_name
    }

    try:
        response = session.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if results:
            poster_path = results[0].get("poster_path")

            if poster_path:
                poster_url = (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

                poster_cache[movie_name] = poster_url

                return poster_url

    except requests.exceptions.RequestException as e:
        print("TMDB API Error:", e)

    placeholder = "https://placehold.co/300x450?text=No+Poster"

    poster_cache[movie_name] = placeholder

    return placeholder
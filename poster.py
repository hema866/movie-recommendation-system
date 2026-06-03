import requests

API_KEY = "9be2139eb7649fcf61b7477464a8269c"

def fetch_poster(movie_name):

    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

    try:

        response = requests.get(url, timeout=10)

        print("Status:", response.status_code)

        data = response.json()

        if data.get("results"):

            poster_path = data["results"][0].get("poster_path")

            if poster_path:
                return (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

        return ""

    except Exception as e:

        print("TMDB Error:", e)

        return ""
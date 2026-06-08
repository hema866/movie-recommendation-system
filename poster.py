import requests

API_KEY = "9be2139eb7649fcf61b7477464a8269c"

def fetch_poster(movie_name):

    print("Searching:", movie_name)

    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_name}"

    try:
        response = requests.get(url, timeout=5)

        print("Status:", response.status_code)

        data = response.json()

        print(data)

        if data.get("results"):

            poster_path = data["results"][0].get("poster_path")

            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path

        return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception as e:

        print("TMDB Error:", e)

        return "https://via.placeholder.com/300x450?text=No+Poster"
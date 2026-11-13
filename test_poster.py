import requests
import time

API_KEY = "9be2139eb7649fcf61b7477464a8269c"

url = "https://api.themoviedb.org/3/search/movie"

params = {
    "api_key": API_KEY,
    "query": "Avatar"
}

for attempt in range(3):

    try:
        print("Attempt:", attempt + 1)

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        print("Status Code:", response.status_code)

        if response.status_code == 200:

            data = response.json()

            poster_path = data["results"][0]["poster_path"]

            poster_url = "https://image.tmdb.org/t/p/w500" + poster_path

            print("Poster URL:", poster_url)

            break

        else:
            print(response.text)

    except requests.exceptions.RequestException as e:

        print("Error:", e)
        time.sleep(3)
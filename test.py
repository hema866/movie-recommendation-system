
import requests

url = "https://api.themoviedb.org/3/search/movie?api_key=9be2139eb7649fcf61b7477464a8269c&query=Avatar"

response = requests.get(url)

print("Status Code:", response.status_code)

if response.status_code == 200:

    data = response.json()

    for movie in data["results"][:5]:

        print("\nMovie Name:", movie["title"])
        print("Release Date:", movie["release_date"])
        print("Overview:", movie["overview"])

        poster = movie["poster_path"]

        if poster:
            poster_url = "https://image.tmdb.org/t/p/w500" + poster
            print("Poster URL:", poster_url)

else:
    print("API request failed!")
import requests

url = "https://api.themoviedb.org/3/search/movie?api_key=9be2139eb7649fcf61b7477464a8269c&query=Avatar"

try:
    r = requests.get(url, timeout=20)
    print(r.status_code)
    print(r.text[:500])

except Exception as e:
    print(e)
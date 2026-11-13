from model import recommend, movies

# Get the first movie from your dataset
movie_name = movies.iloc[0]["Title"]

print("Selected Movie:", movie_name)

# Get recommendations
results = recommend(movie_name)

print("\nRecommended Movies:")

for movie in results:

    print("\nTitle:", movie["Title"])
    print("Genre:", movie["Genre"])
    print("Rating:", movie["Rating"])
    print("Poster:", movie["Poster"])
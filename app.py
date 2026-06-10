from flask import Flask, render_template, request, jsonify
from poster import fetch_poster
from model import (
    recommend,
    mood_recommend,
    hybrid_recommend,
    top_movies,
    trending_movies,
    search_movies,
    advanced_filter,
    movies
)
print(movies.columns.tolist())

app = Flask(__name__)

# -----------------------------
# HOME PAGE
# -----------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -----------------------------
# MOVIE RECOMMENDATION
# -----------------------------
@app.route('/recommend')
def movie_recommendation():

    movie = request.args.get('movie')

    if not movie:
        return jsonify([])

    result = recommend(movie)

    return jsonify(result)


# -----------------------------
# MOOD RECOMMENDATION
# -----------------------------
@app.route('/mood')
def mood():

    mood_name = request.args.get('mood')

    print("Mood received:", mood_name)

    result = mood_recommend(mood_name)

    print("Movies returned:")
    for movie in result:
        print(movie["Title"])

    return jsonify(result)


# -----------------------------
# HYBRID RECOMMENDATION
# -----------------------------
@app.route('/hybrid')
def hybrid():

    movie = request.args.get('movie')
    mood_name = request.args.get('mood')

    if not movie or not mood_name:
        return jsonify([])

    result = hybrid_recommend(
        movie,
        mood_name
    )

    return jsonify(result)


# -----------------------------
# MOVIE INFO
# -----------------------------
@app.route('/movieinfo')
def movie_info():

    movie = request.args.get('movie')

    if not movie:
        return jsonify({})

    data = movies[
        movies['Title'].str.lower()
        ==
        movie.lower()
    ]

    if data.empty:
        return jsonify({})

    row = data.iloc[0]

    return jsonify({

        "Title": row['Title'],
        "Genre": row['Genre'],
        "Language": row['Language'],
        "Rating": row['Rating'],
        "Poster": fetch_poster(
            row['Title']
        )

    })

mood_mapping = {
    "Happy": ["Comedy"],
    "Sad": ["Drama"],
    "Romantic": ["Romance"],
    "Excited": ["Action", "Adventure"]
}

def filter_movies(mood, language, rating, year):

    filtered = movies.copy()

    print("Initial:", len(filtered))

    if mood:
        genres = mood_mapping.get(mood, [])

        filtered = filtered[
            filtered['Genre'].apply(
                lambda x: any(
                    g.lower() in str(x).lower()
                    for g in genres
                )
            )
        ]

        print("After Mood:", len(filtered))

    if language:
        filtered = filtered[
            filtered['Language'].astype(str).str.lower()
            == language.lower()
        ]

        print("After Language:", len(filtered))

    if rating:
        filtered = filtered[
            filtered['Rating'] >= float(rating)
        ]

        print("After Rating:", len(filtered))
    print("Movies before Year filter:")
    print(filtered[['Title', 'Year']].head(30))

    print("Year datatype:", filtered['Year'].dtype)
    print("Max year:", filtered['Year'].max())
    print("Min year:", filtered['Year'].min())
    if year:
        filtered = filtered[
            filtered['Year'] >= float(year)
        ]

        print("After Year:", len(filtered))

    return filtered.head(20)

@app.route('/filter')
def filter_route():

    mood = request.args.get('mood')
    language = request.args.get('language')
    rating = request.args.get('rating')
    year = request.args.get('year')

    results = filter_movies(
        mood,
        language,
        rating,
        year
    )

    print("Mood:", mood)
    print("Language:", language)
    print("Rating:", rating)
    print("Year:", year)

    print("Results Found:", len(results))
    print(results.head())

    movies = []

    for _, row in results.iterrows():

        movies.append({
            "Title": row["Title"],
            "Genre": row["Genre"],
            "Language": row["Language"],
            "Rating": row["Rating"],
            "Poster": "https://via.placeholder.com/300x450?text=Movie"
        })

    return jsonify(movies)

# -----------------------------
# TOP RATED MOVIES
# -----------------------------
@app.route('/top')
def top():

    page = int(request.args.get('page', 1))
    per_page = 5

    result = top_movies()

    total_movies = len(result)

    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        "movies": result[start:end],
        "current_page": page,
        "total_movies": total_movies,
        "has_more": end < total_movies
    })


# -----------------------------
# TRENDING MOVIES
# -----------------------------
@app.route('/trending')
def trending():

    page = int(request.args.get('page', 1))
    per_page = 5

    result = trending_movies()

    total_movies = len(result)

    start = (page - 1) * per_page
    end = start + per_page

    return jsonify({
        "movies": result[start:end],
        "current_page": page,
        "total_movies": total_movies,
        "has_more": end < total_movies
    })


# -----------------------------
# SEARCH AUTOCOMPLETE
# -----------------------------
@app.route('/search')
def search():

    query = request.args.get('q')

    if not query:
        return jsonify([])

    result = search_movies(query)

    return jsonify(result)



# -----------------------------
# GENRE MOVIES WITH PAGINATION
# -----------------------------
@app.route('/genre/<genre>')
def genre_movies(genre):

    page = int(request.args.get('page', 1))
    per_page = 5

    filtered_movies = movies[
        movies['Genre'].str.contains(
            genre,
            case=False,
            na=False
        )
    ]

    total_movies = len(filtered_movies)

    start = (page - 1) * per_page
    end = start + per_page

    page_movies = filtered_movies.iloc[start:end]

    result = []

    for _, row in page_movies.iterrows():

        result.append({
            "Title": row["Title"],
            "Genre": row["Genre"],
            "Language": row.get("Language", ""),
            "Rating": row.get("Rating", ""),
            "Poster": fetch_poster(row["Title"])
        })

    return jsonify({
        "movies": result,
        "current_page": page,
        "total_movies": total_movies,
        "has_more": end < total_movies
    })

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
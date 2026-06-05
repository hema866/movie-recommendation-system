from flask import Flask, render_template, request, jsonify

from model import (
    recommend,
    mood_recommend,
    hybrid_recommend,
    top_movies,
    trending_movies,
    search_movies,
    advanced_filter
)

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
# TOP RATED MOVIES
# -----------------------------
@app.route('/top')
def top():

    result = top_movies()

    return jsonify(result)


# -----------------------------
# TRENDING MOVIES
# -----------------------------
@app.route('/trending')
def trending():

    result = trending_movies()

    return jsonify(result)


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
# ADVANCED FILTER
# -----------------------------
@app.route('/filter')
def filter_movies():

    language = request.args.get('language')
    rating = request.args.get('rating')
    year = request.args.get('year')

    result = advanced_filter(
        language=language,
        min_rating=rating,
        year=year
    )

    return jsonify(result)


# -----------------------------
# RUN APP
# -----------------------------
# -----------------------------
# RUN APP
# -----------------------------
# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
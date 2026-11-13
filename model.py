import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from poster import fetch_poster
# -----------------------------
# LOAD DATASET
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(
    BASE_DIR,
    "dataset",
    "indian_movies.csv"
)

movies = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Total movies:", len(movies))

# -----------------------------
# CLEAN DATA
# -----------------------------
movies = movies[
    ['Movie Name',
     'Genre',
     'Language',
     'Rating(10)',
     'Year',
     'Votes']
].copy()

movies = movies.rename(columns={
    'Movie Name': 'Title',
    'Rating(10)': 'Rating'
})

movies = movies.dropna(
    subset=['Title', 'Genre']
)

# -----------------------------
# CONVERT DATA TYPES
# -----------------------------
movies['Rating'] = pd.to_numeric(
    movies['Rating'],
    errors='coerce'
)

movies['Year'] = pd.to_numeric(
    movies['Year'],
    errors='coerce'
)

movies['Votes'] = (
    movies['Votes']
    .astype(str)
    .str.replace(',', '')
)

movies['Votes'] = pd.to_numeric(
    movies['Votes'],
    errors='coerce'
)

movies['Rating'] = movies['Rating'].fillna(0)
movies['Year'] = movies['Year'].fillna(0)
movies['Votes'] = movies['Votes'].fillna(0)

# -----------------------------
# LIMIT DATASET
# -----------------------------
movies = movies.head(5000)

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------
movies['tags'] = (
    movies['Genre'].fillna('') +
    " " +
    movies['Title'].fillna('')
)

# -----------------------------
# VECTORIZATION
# -----------------------------
cv = CountVectorizer(
    max_features=3000,
    stop_words='english'
)

vectors = cv.fit_transform(
    movies['tags']
)

movies = movies.reset_index(drop=True)

# -----------------------------
# RECOMMEND FUNCTION
# -----------------------------
def recommend(movie):

    matches = movies[
        movies['Title']
        .str.lower()
        ==
        movie.lower()
    ]

    if matches.empty:
        return []

    idx = matches.index[0]

    movie_vector = vectors[idx]

    similarities = cosine_similarity(
        movie_vector,
        vectors
    )[0]

    movie_list = sorted(
        list(enumerate(similarities)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    result = []

    for i in movie_list:

        row = movies.iloc[i[0]]

        result.append({

            "Title": row['Title'],
            "Genre": row['Genre'],
            "Language": row['Language'],
            "Rating": row['Rating'],
            "Poster": fetch_poster(row['Title'])

        })

    return result

# -----------------------------
# MOOD RECOMMEND
# -----------------------------
# -----------------------------
# MOOD RECOMMEND
# -----------------------------

def mood_recommend(mood):

    if not mood:
        return []

    mood = mood.lower().strip()

    # Select movies based on mood
    if mood == "happy":

        data = movies[
            movies['Genre'].str.contains(
                "Comedy|Family",
                case=False,
                na=False
            )
        ]

    elif mood == "sad":

        data = movies[
            movies['Genre'].str.contains(
                "Drama",
                case=False,
                na=False
            )
        ]

    elif mood == "romantic":

        data = movies[
            movies['Genre'].str.contains(
                "Romance",
                case=False,
                na=False
            )
        ]

    elif mood == "action":

        data = movies[
            movies['Genre'].str.contains(
                "Action",
                case=False,
                na=False
            )
        ]

    else:
        return []

    # Select up to 10 random movies
    data = data.sample(
        n=min(10, len(data))
    )

    result = []

    for _, row in data.iterrows():

        result.append({

            "Title": row['Title'],
            "Genre": row['Genre'],
            "Language": row['Language'],
            "Rating": row['Rating'],
            "Poster": fetch_poster(row['Title'])

        })

    return result


# -----------------------------
# HYBRID RECOMMEND
# -----------------------------
# -----------------------------
# HYBRID RECOMMEND
# -----------------------------

def hybrid_recommend(movie, mood):

    # Check empty inputs
    if not movie or not movie.strip():
        return []

    if not mood or not mood.strip():
        return []

    # Get similar movies
    similar_movies = recommend(movie)

    # Get mood-based movies
    mood_movies = mood_recommend(mood)

    # If no similar movies are found
    if not similar_movies:
        return mood_movies[:10]

    # If no mood movies are found
    if not mood_movies:
        return similar_movies[:5]

    # Get titles of mood movies
    mood_titles = [
        m["Title"].lower()
        for m in mood_movies
    ]

    final_movies = []

    # Find movies matching both conditions
    for movie_data in similar_movies:

        if movie_data["Title"].lower() in mood_titles:

            final_movies.append(movie_data)

    # If no common movies are found
    if not final_movies:

        final_movies = similar_movies[:5]

        for mood_movie in mood_movies:

            if mood_movie["Title"].lower() not in [
                m["Title"].lower()
                for m in final_movies
            ]:

                final_movies.append(mood_movie)

            if len(final_movies) >= 10:
                break

    return final_movies[:20]

# -----------------------------
# LANGUAGE FILTER
# -----------------------------
# -----------------------------
# LANGUAGE FILTER
# -----------------------------

def language_filter(language):

    if not language or not language.strip():
        return []

    data = movies[
        movies['Language']
        .fillna('')
        .str.strip()
        .str.lower()
        ==
        language.strip().lower()
    ]

    return data[
        ['Title', 'Language', 'Genre', 'Rating']
    ].head(20).to_dict('records')


# -----------------------------
# RATING FILTER
# -----------------------------

def rating_filter(min_rating):

    try:
        min_rating = float(min_rating)
    except (ValueError, TypeError):
        return []

    data = movies[
        movies['Rating'] >= min_rating
    ]

    return data[
        ['Title', 'Genre', 'Language', 'Rating']
    ].sort_values(
        by='Rating',
        ascending=False
    ).head(20).to_dict('records')

# -----------------------------
# YEAR FILTER
# -----------------------------

def year_filter(min_year):

    try:
        min_year = int(min_year)
    except (ValueError, TypeError):
        return []

    data = movies[
        movies['Year'] >= min_year
    ]

    return data[
        ['Title', 'Year', 'Genre', 'Language', 'Rating']
    ].sort_values(
        by='Year',
        ascending=False
    ).head(20).to_dict('records')

# -----------------------------
# ADVANCED FILTER
# -----------------------------

def advanced_filter(
        language=None,
        min_rating=None,
        year=None):

    data = movies.copy()

    # Filter by language
    if language and language.strip():

        data = data[
            data['Language']
            .fillna('')
            .str.strip()
            .str.lower()
            ==
            language.strip().lower()
        ]

    # Filter by minimum rating
    if min_rating is not None and min_rating != '':

        try:
            min_rating = float(min_rating)

            data = data[
                data['Rating'] >= min_rating
            ]

        except (ValueError, TypeError):
            return []

    # Filter by release year
    if year is not None and year != '':

        try:
            year = int(year)

            data = data[
                data['Year'] >= year
            ]

        except (ValueError, TypeError):
            return []

    # Sort results by rating
    data = data.sort_values(
        by='Rating',
        ascending=False
    )

    return data[
        ['Title', 'Language', 'Genre', 'Rating', 'Year']
    ].head(20).to_dict('records')


# -----------------------------
# TOP MOVIES
# -----------------------------
# -----------------------------
# TOP MOVIES
# -----------------------------

def top_movies():

    data = movies.sort_values(
        by='Rating',
        ascending=False
    ).head(20)

    result = []

    for _, row in data.iterrows():

        result.append({

            "Title": row['Title'],
            "Genre": row['Genre'],
            "Language": row['Language'],
            "Rating": row['Rating'],
            "Poster": fetch_poster(row['Title'])

        })

    return result


# -----------------------------
# TRENDING MOVIES
# -----------------------------
# -----------------------------
# TRENDING MOVIES
# -----------------------------

def trending_movies():

    data = movies.sort_values(
        by='Votes',
        ascending=False
    ).head(20)

    result = []

    for _, row in data.iterrows():

        result.append({

            "Title": row['Title'],
            "Genre": row['Genre'],
            "Language": row['Language'],
            "Rating": row['Rating'],
            "Poster": fetch_poster(row['Title'])

        })

    return result


# -----------------------------
# SEARCH MOVIES
# -----------------------------
def search_movies(query):

    if not query or not query.strip():
        return []

    data = movies[
        movies['Title'].str.contains(
            query,
            case=False,
            na=False,
            regex=False
        )
    ]

    return data[
        ['Title', 'Language', 'Rating']
    ].head(10).to_dict('records')
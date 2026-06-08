import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from poster import fetch_poster
# -----------------------------
# LOAD DATASET
# -----------------------------
file_path = os.path.join("dataset", "indian_movies.csv")

movies = pd.read_csv(file_path)

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
def mood_recommend(mood):

    mood = mood.lower().strip()

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
        data = movies

    # Select up to 10 random movies
    data = data.sort_values(
        by='Rating',
        ascending=False
    ).head(10)

    print(f"\nSelected Mood: {mood}")
    print(data[['Title', 'Genre']])

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
def hybrid_recommend(movie, mood):

    similar_movies = recommend(movie)

    mood_movies = mood_recommend(mood)

    mood_titles = [
        m["Title"]
        for m in mood_movies
    ]

    final_movies = []

    for movie_data in similar_movies:

        if movie_data["Title"] in mood_titles:

            final_movies.append(movie_data)

    if len(final_movies) == 0:

        final_movies = similar_movies[:5]

        for mood_movie in mood_movies:

            if mood_movie["Title"] not in [
                m["Title"]
                for m in final_movies
            ]:

                final_movies.append(mood_movie)

            if len(final_movies) >= 10:
                break

    return final_movies

# -----------------------------
# LANGUAGE FILTER
# -----------------------------
def language_filter(language):

    data = movies[
        movies['Language']
        .str.lower()
        ==
        language.lower()
    ]

    return data[
        ['Title',
         'Language',
         'Genre',
         'Rating']
    ].head(20)


# -----------------------------
# RATING FILTER
# -----------------------------
def rating_filter(min_rating):

    data = movies[
        movies['Rating']
        >= min_rating
    ]

    return data[
        ['Title',
         'Genre',
         'Language',
         'Rating']
    ].sort_values(
        by='Rating',
        ascending=False
    ).head(20)


# -----------------------------
# YEAR FILTER
# -----------------------------
def year_filter(min_year):

    data = movies[
        movies['Year']
        >= min_year
    ]

    return data[
        ['Title',
         'Year',
         'Genre',
         'Language',
         'Rating']
    ].sort_values(
        by='Year',
        ascending=False
    ).head(20)


# -----------------------------
# ADVANCED FILTER
# -----------------------------
def advanced_filter(
        language=None,
        min_rating=None,
        year=None):

    data = movies.copy()

    if language:

        data = data[
            data['Language']
            .str.lower()
            ==
            language.lower()
        ]

    if min_rating:

        data = data[
            data['Rating']
            >= float(min_rating)
        ]

    if year:

        data = data[
            data['Year']
            >= int(year)
        ]

    return data[
        ['Title',
         'Language',
         'Genre',
         'Rating',
         'Year']
    ].sort_values(
        by='Rating',
        ascending=False
    ).head(20).to_dict('records')


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

    data = movies[
        movies['Title']
        .str.contains(
            query,
            case=False,
            na=False
        )
    ]

    return data[
        ['Title',
         'Language',
         'Rating']
    ].head(10).to_dict('records')
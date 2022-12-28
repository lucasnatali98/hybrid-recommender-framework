import pandas as pd
from src.preprocessing.text import TextProcessing
from src.data.movielens import MovieLens
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer
"""
Esse exemplo foi extraido do seguinte tutorial:

https://medium.com/analytics-vidhya/content-based-recommender-systems-in-python-2b330e01eb80

"""
movielens = MovieLens({
    'proportion': 'ml-latest-small',
    'filters': {}
})

movies = movielens.items


text_processing = TextProcessing({
    'apply_on': {
        'movies': ['genres'],
        'tags': ['']
    },
    'dataset': 'movielens',
})

tfidf = TfidfVectorizer(stop_words='english')
movies['genres'] = movies['genres'].apply(
    lambda x: x.replace("|", " ")
)

genres_matrix = tfidf.fit_transform(movies['genres'])
print("genres matrix shape: ", genres_matrix.shape)


similarity_matrix = linear_kernel(genres_matrix, genres_matrix)
print("similarity matrix")
print(similarity_matrix)


mapping = pd.Series(movies.index, index=movies['title'])
print("Mapping")
print(mapping)

def recommend_movies(movie_input):
    movie_index = mapping[movie_input]
    similarity_score = list(enumerate(similarity_matrix[movie_index]))
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    similarity_score = similarity_score[1:15]
    movie_indices = [i[0] for i in similarity_score]
    return movies['title'].iloc[movie_indices]

print("Recommendations:")
recommendations = recommend_movies("Toy Story (1995)")
print(recommendations)
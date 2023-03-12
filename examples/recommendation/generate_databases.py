from src.data.movielens import MovieLens

ratings = MovieLens({
    'proportion': "ml-latest"
}).ratings

ratings200k = ratings.sample(200000)
ratings300k = ratings.sample(300000)
ratings400k = ratings.sample(400000)

ratings200k.to_csv("ratings-200k.csv")
ratings300k.to_csv("ratings-300k.csv")
ratings400k.to_csv("ratings-400k.csv")
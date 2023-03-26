from academic.bcc409.p2022_2.grupo3.lastFM2 import LastFM2
from src.preprocessing.normalize import NormalizeProcessing
from src.recommenders.item_knn import LenskitItemKNN
import numpy as np

lastFM = LastFM2({
    'proportion': "lastFM2"
})
ratings = LastFM2.ratings
artists = LastFM2.items
# normalize_processing = NormalizeProcessing({
#     'norm': 'max',
#     'column_to_apply': "rating",
#     'axis': 0
# })

# normalizedRatings = normalize_processing.pre_processing(ratings)
item_knn = LenskitItemKNN({
    'maxNumberNeighbors': 10,
})

# normalizedRatings = normalizedRatings[normalizedRatings['rating'].notna()]
# print(normalizedRatings)
items = ratings['item'].values
users = ratings['user'].values
unique_users = np.unique(users)

user = unique_users[0]
item_knn.fit(ratings)

predict_to_user = item_knn.predict_for_user(user, items)
predict_to_user = predict_to_user[predict_to_user.notna()]

print("Predict to user")
print(user)
print(predict_to_user)

predict = item_knn.predict(ratings[['user', 'item']])
print("Predict")
print(predict)

recommend_to_users = item_knn.recommend(unique_users, 10)
recommend_to_users = recommend_to_users[recommend_to_users['score'].notna()]
print("Recommend")
print(recommend_to_users)
recommend_to_users.to_csv("recommend_to_users.csv")

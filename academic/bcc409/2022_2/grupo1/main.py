import pandas as pd

from src.preprocessing.split import SplitProcessing
from src.preprocessing.folds import FoldsProcessing
from src.recommenders.random_item import RandomItem
from src.recommenders.user_knn import UserKNN
from src.metrics.rmse import LenskitRMSE

from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from sklearn import linear_model
#numpy.flatten

data_frame = pd.read_csv("data.csv")

data_frame.drop(columns=['ID', 'Start time', 'Completion time'],inplace=True)
#print(data_frame)

#turns data into numbers and
#creates new columns
data_frame['gender_n'] = LabelEncoder().fit_transform(data_frame['Select your Gender :'])
data_frame['age_n'] = LabelEncoder().fit_transform(data_frame['Select your age :'])
data_frame['spicy_n'] = LabelEncoder().fit_transform(data_frame['How much spicy would you like your pizza to be?'])
data_frame['pepperoni_n'] = LabelEncoder().fit_transform(data_frame['Do you like Pepperoni ?'])
data_frame['chicken_grain_n'] = LabelEncoder().fit_transform(data_frame['Which one do you prefer the most :'])
data_frame['tomato_n'] = LabelEncoder().fit_transform(data_frame['Do you Prefer Tomatoes?'])
data_frame['olives_n'] = LabelEncoder().fit_transform(data_frame['Which one of these do you like ?'])
data_frame['capsicum_n'] = LabelEncoder().fit_transform(data_frame['Do you like Capsicum ?'])
data_frame['beef_chicken_n'] = LabelEncoder().fit_transform(data_frame['Which one of these you like ?'])
data_frame['peppers_n'] = LabelEncoder().fit_transform(data_frame['Do you like Peppers ?'])
data_frame['sauce_n'] = LabelEncoder().fit_transform(data_frame['Do you like Sauce :'])
data_frame['mushroom_n'] = LabelEncoder().fit_transform(data_frame['Do you like Mushroom :'])
data_frame['pesto_n'] = LabelEncoder().fit_transform(data_frame['Do you like Pesto :'])
data_frame['cheese_n'] = LabelEncoder().fit_transform(data_frame['Do you like Cheese :'])
data_frame['health_n'] = LabelEncoder().fit_transform(data_frame['Have any Health or diet issue ?'])

# delete old columns
data_frame_n = data_frame.drop(['Select your Gender :', 'Select your age :', 'How much spicy would you like your pizza to be?', 'Do you like Pepperoni ?', 'Which one do you prefer the most :','Do you Prefer Tomatoes?', 'Which one of these do you like ?','Do you like Capsicum ?', 'Which one of these you like ?', 'Do you like Peppers ?', 'Do you like Sauce :', 'Do you like Mushroom :', 'Do you like Pesto :',  'Do you like Cheese :','Have any Health or diet issue ?' ], axis='columns')
#print(data_frame_n)

'''split_processing = SplitProcessing({
                "target": "tomato_n",
                "train_size": 70,
                "test_size": 30,
                "random_state": 42,
                "shuffle": "",
                "stratify": ""
})

split_processing.pre_processing(data_frame_n)'''

#usar k fold

k_fold = FoldsProcessing({
        "target_column": "tomato_n",
        "folds": 5,
        "shuffle": False,
        "random_state": 42,
        "strategy": "kfold"
})
k_fold.pre_processing(data_frame_n)

x_train = pd.read_csv("/home/clara/PycharmProjects/hybrid_recommender_framework/experiment_output/preprocessing/xtrain.csv")
y_train = pd.read_csv("/home/clara/PycharmProjects/hybrid_recommender_framework/experiment_output/preprocessing/ytrain.csv")
x_test = pd.read_csv("/home/clara/PycharmProjects/hybrid_recommender_framework/experiment_output/preprocessing/xtest.csv")
y_test = pd.read_csv("/home/clara/PycharmProjects/hybrid_recommender_framework/experiment_output/preprocessing/ytest.csv")


print("=================================== LINEAR REGRESSION ===================================")
reg_tomato = linear_model.LinearRegression()
reg_tomato.fit(x_train, y_train)
predict_lr = reg_tomato.predict(x_test)
score_lr = reg_tomato.score(x_test,y_test)

print(f'[LINEAR REGRESSION] Score: {}', score_lr)
print(f'[LINEAR REGRESSION] Predict: {}', predict_lr)


print("========================================== RMSE ==========================================")
rmse = LenskitRMSE({
        "sample_weight": "None",
        "squared": True,
        "missing": "error"
})
score_rmse = rmse.evaluate(predict, y_test.values)
print(f'[RMSE] Score: {}', score_rmse)



print("=================================== DECISION TREE ===================================")
model_tomato = tree.DecisionTreeClassifier()
model_tomato.fit(x_train, y_train) #target (y) is the answer

model_tomato.predict(x_test)
score_tomato_dt = model_tomato.score(x_test,y_test)
print(f'[DECISION TREE] Score: {}', score_tomato_dt)



print("========================== CONTENT-BASED RECOMMENDER SYSTEM ==========================")
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

mapping = pd.Series(data_frame_n.index[0], index=[row for row in data_frame_n])
print(f'\n[CONTENT BASED] Mapping: \n{mapping}')

ing_index = mapping["tomato_n"]
similarity_score = list(enumerate(similarity_matrix[ing_index]))
print(f'\n[CONTENT BASED] Similarity Score: \n{similarity_score}')

similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
similarity_score = similarity_score[1:15]
ing_indices = [i[0] for i in similarity_score]
print(f'\n[CONTENT BASED] Result recommendations for TOMATO: \n{data_frame_n.iloc[ing_indices]}')
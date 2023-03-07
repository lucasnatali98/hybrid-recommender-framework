import pandas as pd

from src.preprocessing.split import SplitProcessing
from src.recommenders.random_item import RandomItem
from src.recommenders.user_knn import UserKNN

from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from sklearn import linear_model

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

split_processing = SplitProcessing({
                "target": "tomato_n",
                "train_size": 70,
                "test_size": 30,
                "random_state": 42,
                "shuffle": "",
                "stratify": ""
})

split_processing.pre_processing(data_frame_n)
#usar k fold

x_train = pd.read_csv("/home/clara/PycharmProjects/hybrid_recommender_framework/experiment_output/preprocessing/xtrain.csv")
y_train = pd.read_csv("/home/clara/PycharmProjects/hybrid_recommender_framework/experiment_output/preprocessing/ytrain.csv")
x_test = pd.read_csv("/home/clara/PycharmProjects/hybrid_recommender_framework/experiment_output/preprocessing/xtest.csv")
y_test = pd.read_csv("/home/clara/PycharmProjects/hybrid_recommender_framework/experiment_output/preprocessing/ytest.csv")

#print(y_train)

#TESTING TOMATO (linear regression))
reg_tomato = linear_model.LinearRegression()
reg_tomato.fit(x_train, y_train)
predict = reg_tomato.predict(x_test)
score = reg_tomato.score(x_test,y_test)
print(score)
#print(predict)
#rmse


#TESTING TOMATO (decision tree))
model_tomato = tree.DecisionTreeClassifier()
model_tomato.fit(x_train, y_train) #target (y) is the answer

model_tomato.predict(x_test)
score_tomato_dt = model_tomato.score(x_test,y_test)
print(score_tomato_dt)

#TESTING TOMATO (random item))
#tomato_random_item = RandomItem({})

#TESTING TOMATO (knn user))
tomato_knn_user = UserKNN({
    "maxNumberNeighbors": 12,
})
from scipy.stats import uniform as uniform
from scipy.stats import randint as randint
from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import Ridge
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import SGDRegressor
from sklearn.isotonic import IsotonicRegression
from sklearn.ensemble import BaggingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import LinearSVR
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from operator import itemgetter


class ScikitTuning:

    def __init__(self):
        pass

    def define_algorithms(self, algorithms):
        pass

    def report(self, search):
        pass

    def fit(self):
        pass

    def save_results(self):
        pass

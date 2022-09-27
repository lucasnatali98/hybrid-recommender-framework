from sklearn.model_selection import train_test_split
from src.preprocessing.preprocessing import AbstractPreProcessing


"""
Estrategias de Fold:

K-Fold
StratifiedKFold
GroupKFold
ShuffleSplit
StratifiedShuffleSplit
GroupShuffleSplit
LeaveOneOut
LeavePOut

"""

class SplitProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict):
        """
        
        """

        super().__init__()

    def pre_processing(self, data, **kwargs):
        """

        @param **kwargs:
        @param data:
        @return:
        """
        X_train, X_test, y_train, y_test = train_test_split(data, [2,3,4], test_size=0.2)

        return X_train, X_test, y_train, y_test

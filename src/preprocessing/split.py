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
        test_size = kwargs.pop('test_size')
        train_size = kwargs.pop('train_size')
        random_state = kwargs.pop('random_state')
        shuffle = kwargs.pop('shuffle')
        stratify = kwargs.pop('stratify')

        X_train, X_test, y_train, y_test = train_test_split(
            data,
            train_size=train_size,
            test_size=test_size,
            random_state=random_state,
            shuffle=shuffle,
            stratify=stratify
        )

        return X_train, X_test, y_train, y_test

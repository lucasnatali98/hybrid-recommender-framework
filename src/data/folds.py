from abc import ABC, abstractmethod
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, StratifiedKFold, StratifiedShuffleSplit
from sklearn.model_selection import StratifiedGroupKFold, KFold, ShuffleSplit


class Strategy(ABC):

    @abstractmethod
    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        pass


class Folds:
    def __init__(self, strategy: str) -> None:
        possible_strategies = {
            "stratifiedkfolds": StratifiedKFold,
            "kfold": KFoldStrategy,
            "stratifiedshufflesplit": StratifiedShuffleSplitStrategy,
            "stratifiedgroupkfolds": StratifiedGroupKFoldsStrategy
        }

        strategy_class = possible_strategies[strategy]
        self._strategy = strategy_class

    @property
    def strategy(self) -> Strategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs) -> None:
        """

        @return:
        """
        result = self._strategy.create_folds(self, data=data,
                                             n_splits=n_splits,
                                             shuffle=shuffle,
                                             random_state=random_state)
        return result


class KFoldStrategy(Strategy):
    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int = None, **kwargs):
        print('Create folds in KFold Strategy')
        kfold = KFold(n_splits=n_splits, shuffle=shuffle)
        kfold_n_splits = kfold.get_n_splits(data)
        for train_index, test_index in kfold.split(data):
            print("TRAIN:", train_index, "TEST:", test_index)


        return None



class GroupKFoldStrategy(Strategy):
    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        print('Create folds in GroupKFold Strategy')
        group_kfold = GroupKFold(n_splits=n_splits)
        return group_kfold


class StratifiedGroupKFoldsStrategy(Strategy):
    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        print('Create folds in StratifiedGroupKFolds Strategy')
        stratified_group_kfolds = StratifiedGroupKFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
        return stratified_group_kfolds


class StratifiedShuffleSplitStrategy(Strategy):

    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        print('Create folds in StratifiedShuffleSPlit Strategy')
        stratified_shuffle_split = StratifiedShuffleSplit(n_splits=n_splits, random_state=random_state)
        return stratified_shuffle_split


class ShuffleSplitStrategy(Strategy):

    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        print('Create folds in ShuffleSplit Strategy')
        shuffle_split = ShuffleSplit(n_splits=n_splits, random_state=random_state)
        return shuffle_split

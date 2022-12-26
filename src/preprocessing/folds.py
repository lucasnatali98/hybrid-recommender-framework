from abc import ABC, abstractmethod
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, StratifiedKFold, StratifiedShuffleSplit
from sklearn.model_selection import StratifiedGroupKFold, KFold, ShuffleSplit
from src.preprocessing.preprocessing import AbstractPreProcessing


class Strategy(ABC):

    @abstractmethod
    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        pass


class FoldsProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict) -> None:
        super().__init__()

        parameters = self.process_parameters(parameters)
        self.number_of_folds = parameters['folds']
        self.strategy = parameters['strategy']
        self.shuffle = parameters['shuffle']
        self.random_state = parameters['random_state']

    def process_parameters(self, parameters: dict) -> dict:
        default_keys = [
            'folds',
            'strategy'
        ]

        for key in parameters.keys():
            if key not in default_keys:
                raise KeyError("Você não informou a chave {} e ela é obrigatória".format(key))

        return parameters

    def pre_processing(self, data, **kwargs):
        folds = Folds(self.strategy)

        result = folds.create_folds(
            data=data,
            n_splits=self.number_of_folds,
            shuffle=self.shuffle,
            random_state=self.random_state
        )

        return result


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

    def save_folds(self, X, y, train_indexes, test_indexes):
        """

        @param X:
        @param y:
        @param train_indexes:
        @param test_indexes:
        @return:
        """
        pass

    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
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
        """

        @param data:
        @param n_splits:
        @param shuffle:
        @param random_state:
        @param kwargs:
        @return:
        """
        print('Create folds in KFold Strategy')
        kfold = KFold(n_splits=n_splits, shuffle=shuffle)
        return kfold


class GroupKFoldStrategy(Strategy):
    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        """

        @param data:
        @param n_splits:
        @param shuffle:
        @param random_state:
        @param kwargs:
        @return:
        """
        print('Create folds in GroupKFold Strategy')
        group_kfold = GroupKFold(n_splits=n_splits)
        return group_kfold


class StratifiedGroupKFoldsStrategy(Strategy):
    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        """

        @param data:
        @param n_splits:
        @param shuffle:
        @param random_state:
        @param kwargs:
        @return:
        """
        print('Create folds in StratifiedGroupKFolds Strategy')
        stratified_group_kfolds = StratifiedGroupKFold(n_splits=n_splits, shuffle=shuffle, random_state=random_state)
        return stratified_group_kfolds


class StratifiedShuffleSplitStrategy(Strategy):

    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        """

        @param data:
        @param n_splits:
        @param shuffle:
        @param random_state:
        @param kwargs:
        @return:
        """
        print('Create folds in StratifiedShuffleSPlit Strategy')
        stratified_shuffle_split = StratifiedShuffleSplit(n_splits=n_splits, random_state=random_state)
        return stratified_shuffle_split


class ShuffleSplitStrategy(Strategy):

    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        """

        @param data:
        @param n_splits:
        @param shuffle:
        @param random_state:
        @param kwargs:
        @return:
        """
        print('Create folds in ShuffleSplit Strategy')
        shuffle_split = ShuffleSplit(n_splits=n_splits, random_state=random_state)
        return shuffle_split


class StratifiedKFoldStrategy(Strategy):
    def create_folds(self, data, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        """

        @param data:
        @param n_splits:
        @param shuffle:
        @param random_state:
        @param kwargs:
        @return:
        """
        print('Create folds in StratifiedKFold Strategy')
        stratified_kfold = StratifiedKFold(n_splits=n_splits, shuffle=shuffle)
        return stratified_kfold

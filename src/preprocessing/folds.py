from abc import ABC, abstractmethod
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, StratifiedKFold, StratifiedShuffleSplit
from sklearn.model_selection import StratifiedGroupKFold, KFold, ShuffleSplit
from src.preprocessing.preprocessing import AbstractPreProcessing
from src.utils import process_parameters, hrf_experiment_output_path


class Strategy(ABC):

    @abstractmethod
    def create_folds(self, X, y, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        pass


class FoldsProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict) -> None:
        super().__init__()
        default_keys = {
            'folds',
            'strategy'
        }
        parameters = process_parameters(parameters, default_keys)
        self.number_of_folds = parameters['folds']
        self.strategy = parameters.get('strategy')
        self.shuffle = parameters.get('shuffle')
        self.random_state = parameters.get('random_state')

    def pre_processing(self, data, **kwargs):
        folds = Folds(self.strategy)
        X = data
        y = data['rating']
        folds_indexes = folds.create_folds(
            X=X,
            y=y,
            n_splits=self.number_of_folds,
            shuffle=self.shuffle,
            random_state=self.random_state
        )
        print("folds preprocessing")

        folds_output_directory = "preprocessing/folds"
        train_folds_output_directory = hrf_experiment_output_path().joinpath(folds_output_directory)
        validation_folds_output_directory = hrf_experiment_output_path().joinpath(folds_output_directory)

        train_folds_output_directory = train_folds_output_directory.joinpath("train/")
        validation_folds_output_directory = validation_folds_output_directory.joinpath("validation/")

        fold_counter = 1
        for train_index, validation_index in folds_indexes:
            train_df = data.loc[train_index, :]
            validation_df = data.loc[validation_index, :]

            train_folds_archive_name = train_folds_output_directory.joinpath("train-fold-{}.csv".format(fold_counter))
            validation_folds_archive_name = validation_folds_output_directory.joinpath(
                "validation-fold-{}.csv".format(fold_counter))

            train_df.to_csv(train_folds_archive_name)
            validation_df.to_csv(validation_folds_archive_name)
            fold_counter = fold_counter + 1


        return data


class Folds:
    def __init__(self, strategy: str) -> None:
        possible_strategies = {
            "stratifiedkfolds": StratifiedKFoldStrategy,
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

    def create_folds(self, X, y, n_splits: int, shuffle: bool, random_state: int, **kwargs):
        """

        @return:
        """
        result = self._strategy.create_folds(self, X=X,
                                             y = y,
                                             n_splits=n_splits,
                                             shuffle=shuffle,
                                             random_state=random_state)
        return result


class KFoldStrategy(Strategy):
    def create_folds(self, X, y, n_splits: int, shuffle: bool, random_state: int = None, **kwargs):
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
        return kfold.split(
            X=X,
            y=y
        )


class GroupKFoldStrategy(Strategy):
    def create_folds(self, X, y, n_splits: int, shuffle: bool, random_state: int, **kwargs):
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
        return group_kfold.split(
            X=X,
            y=y
        )


class StratifiedGroupKFoldsStrategy(Strategy):
    def create_folds(self, X, y, n_splits: int, shuffle: bool, random_state: int, **kwargs):
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
        return stratified_group_kfolds.split(
            X=X,
            y=y
        )


class StratifiedShuffleSplitStrategy(Strategy):

    def create_folds(self, X, y, n_splits: int, shuffle: bool, random_state: int, **kwargs):
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
        return stratified_shuffle_split.split(
            X=X,
            y=y
        )


class ShuffleSplitStrategy(Strategy):

    def create_folds(self, X, y, n_splits: int, shuffle: bool, random_state: int, **kwargs):
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
        return shuffle_split.split(
            X=X,
            y=y
        )


class StratifiedKFoldStrategy(Strategy):
    def create_folds(self, X, y, n_splits: int, shuffle: bool, random_state: int, **kwargs):
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
        return stratified_kfold.split(
            X=X,
            y=y
        )

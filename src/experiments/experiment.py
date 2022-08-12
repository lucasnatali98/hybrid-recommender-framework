from abc import ABC, abstractmethod


class Experiment(ABC):
    @abstractmethod
    def run(self):
        """

        @return:
        """
        pass

    @abstractmethod
    def set_experiments(self, experiments):
        """

        @param experiments:
        @return:
        """
        pass

    @abstractmethod
    def add(self, experiment):
        """

        @param experiment:
        @return:
        """
        pass

    @abstractmethod
    def insert(self, experiments):
        """

        @param experiments:
        @return:
        """
        pass

    @abstractmethod
    def remove(self, experiment):
        """

        @param experiment:
        @return:
        """
        pass

    @abstractmethod
    def removeAll(self):
        """

        @return:
        """
        pass


class ExperimentHandler(Experiment):

    def __init__(self):
        """
        
        """
        self.experiments = []

    def run(self):
        """

        @return:
        """
        pass

    def set_experiments(self, experiments):
        """

        @param experiments:
        @return:
        """
        pass

    def add(self, experiment):
        """

        @param experiment:
        @return:
        """
        pass

    def insert(self, experiments):
        """

        @param experiments:
        @return:
        """
        pass

    def remove(self, experiment):
        """

        @param experiment:
        @return:
        """
        pass

    def removeAll(self):
        """

        @return:
        """
        pass

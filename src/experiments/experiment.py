from abc import ABC, abstractmethod
from src.instance_factory import InstanceFactory


class Experiment(ABC):


    @abstractmethod
    def run(self):
        """

        @return:
        """
        pass

    @abstractmethod
    def set_experiment(self, experiment: dict):
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



from abc import ABC, abstractmethod


class Experiment(ABC):
    @abstractmethod
    def run(self):
        """
        
        """
        pass

    @abstractmethod
    def set_experiments(self, experiments):
        """
        
        """
        pass

    @abstractmethod
    def add(self, experiment):
        """
        
        """
        pass

    @abstractmethod
    def insert(self, experiments):
        """
        
        """
        pass

    @abstractmethod
    def remove(self, experiment):
        """
        
        """
        pass

    @abstractmethod
    def removeAll(self):
        """
        
        """
        pass


class ExperimentHandler(Experiment):

    def __init__(self):
        """
        
        """
        self.experiments = []

    def run(self):
        """
        
        """
        pass

    def set_experiments(self, experiments):
        """
        
        """
        pass

    def add(self, experiment):
        """
        
        """
        pass

    def insert(self, experiments):
        """
        
        """
        pass

    def remove(self, experiment):
        """
        
        """
        pass

    def removeAll(self):
        """
        
        """
        pass

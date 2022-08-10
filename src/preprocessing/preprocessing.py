from abc import ABC, abstractmethod
import sklearn
from src.utils import object_equals_type


class PreProcessing(ABC):

    @abstractmethod
    def pre_processing(self, data):
        """
        
        """
        pass


class AbstractPreProcessing(PreProcessing):

    def __init__(self):
        """
        
        """
        pass

    @abstractmethod
    def pre_processing(self, data):
        """
        
        """
        pass


class PreProcessingContainer:
    preprocessingObjects: [PreProcessing]

    def __init__(self):
        self.processingObjects = []

    def push(self, obj):
        """

        """

        obj_is_instance = isinstance(obj, PreProcessing)

        if obj_is_instance:
            self.processingObjects.insert(-1, obj)
        else:
            raise Exception("")

    def insert(self, obj, index):
        """
        
        """
        obj_is_instance = isinstance(obj, PreProcessing)

        if not obj_is_instance:
            raise Exception("")

        if index > len(self.processingObjects):
            raise Exception("")

        self.processingObjects.insert(index, obj)

    def remove(self, obj):
        """
        
        """
        obj_is_instance = isinstance(obj, PreProcessing)

        if not obj_is_instance:
            raise Exception("")

        self.processingObjects.remove(obj)

    def removeAll(self):
        """
        
        """
        self.processingObjects.clear()

    def print_instances(self):
        for i in self.processingObjects:
            print(i)

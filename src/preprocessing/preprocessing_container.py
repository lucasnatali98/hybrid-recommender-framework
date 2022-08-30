from src.preprocessing.factories import *


class PreProcessingContainer:
    """
    Preciso receber os parametros


    -> O tipo do parametro precisa ser padronizado

    -> toda classe precisa ter um método para interpretar

    https://stackoverflow.com/questions/4821104/dynamic-instantiation-from-string-name-of-a-class-in-dynamically-imported-module
    """

    def __init__(self, parameters: dict):
        """
        @type stages: list

        """
        stages = parameters['stages']

        if len(stages) == 0:
            self.processingObjects = []
        else:
            self.processingObjects = []
            self.processing_factory = ProcessingFactory(parameters)
            self.processingObjects = self.processing_factory.create



    def push(self, obj):
        """
        Insere um objeto do tipo PreProcessing no array


        @param obj:
        @return:
        """

        obj_is_instance = isinstance(obj, PreProcessing)

        if obj_is_instance:
            self.processingObjects.insert(-1, obj)
        else:
            raise Exception("")

    def insert(self, obj, index):
        """

        @param obj:
        @param index:
        @return:
        """
        obj_is_instance = isinstance(obj, PreProcessing)

        if not obj_is_instance:
            raise Exception("")

        if index > len(self.processingObjects):
            raise Exception("")

        self.processingObjects.insert(index, obj)

    def remove(self, obj):
        """

        @param obj:
        @return:
        """
        obj_is_instance = isinstance(obj, PreProcessing)

        if not obj_is_instance:
            raise Exception("")

        self.processingObjects.remove(obj)

    def removeAll(self):
        """

        @return:
        """
        self.processingObjects.clear()

    def print_instances(self):
        """

        @return:
        """
        for i in self.processingObjects:
            print(i)

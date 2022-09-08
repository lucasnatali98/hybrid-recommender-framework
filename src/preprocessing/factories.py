from abc import ABC, abstractmethod
import importlib
from src.preprocessing.preprocessing import AbstractPreProcessing
from src.utils import is_structure_empty

"""
1. Generalizar as fabricas em uma classe
"""


class Creator(ABC):

    @abstractmethod
    def create(self) -> AbstractPreProcessing:
        pass


class ProcessingFactory(Creator):
    def __init__(self, parameters: dict):
        self.parameters = self._handle_config_obj(parameters)

    def _handle_config_obj(self, parameters: dict) -> dict:
        """
        Tem como objetivo verificar a validade do arquivo de configuração para a execução
        das etapas de pré-processamento

        @type parameters: object
        @param config_obj:
        @return: object or None
        """
        stages = parameters['instances']

        is_empty = is_structure_empty(stages)

        if is_empty:
            raise Exception("Não foram inseridos estágios de pré-processamento, esse array não deve estar vazio")

        return parameters


    @property
    def create(self):
        """
        Cria uma instância de um objeto do tipo PreProcessing

        @return: object
        """

        instances = []
        for stages in self.parameters['instances']:
            class_module = stages['module']
            class_name = stages['class_name']

            module = importlib.import_module(class_module)
            class_ = getattr(module, class_name)

            instance = class_(stages['parameters'])
            instances.append(instance)

        return instances

from abc import ABC, abstractmethod
from src.metafeatures.metafeature import MetaFeature
import importlib


class Creator(ABC):

    @abstractmethod
    def create(self) -> MetaFeature:
        pass


class MetafeatureFactory(Creator):
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

        metafeatures = parameters['metafeatures']

        is_empty = self._is_metafeatures_empty(metafeatures)
        if is_empty:
            raise Exception("Não foram inseridos estágios de pré-processamento, esse array não deve estar vazio")

        return parameters

    def _is_metafeatures_empty(self, metafeatures: list) -> bool:
        """
        Verifica se a lista de estágios de preprocessamento está vazia

        @param stages:
        @return:
        """
        if len(metafeatures) == 0:
            return True

        return False

    @property
    def create(self):
        """
        Cria uma instância de um objeto do tipo PreProcessing

        @return: object
        """
        instances = []
        for stages in self.parameters:
            module = importlib.import_module('src.metafeatures')
            class_ = getattr(module, stages['class_name'])
            instance = class_(stages['parameters'])
            instances.append(instance)

        return instances

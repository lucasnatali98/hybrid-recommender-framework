from abc import abstractmethod
from src.recommenders.recommender import Recommender
import importlib


class Creator:

    @abstractmethod
    def create(self) -> Recommender:
        pass


class RecommenderFactory(Creator):
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

        recommenders = parameters['recommenders']

        is_empty = self._is_recommenders_empty(recommenders)
        if is_empty:
            raise Exception("Não foram inseridos estágios de pré-processamento, esse array não deve estar vazio")

        return parameters

    def _is_recommenders_empty(self, recommenders: list) -> bool:
        """
        Verifica se a lista de estágios de preprocessamento está vazia

        @param stages:
        @return:
        """
        if len(recommenders) == 0:
            return True

        return False

    @property
    def create(self):
        """
        Cria uma instância de um objeto do tipo PreProcessing

        @return: object
        """
        instances = []
        for stages in self.parameters['recommenders']:
            class_file = stages['class_file']
            module = importlib.import_module('src.recommenders.' + class_file)
            class_ = getattr(module, stages['class_name'])
            instance = class_(stages['parameters'])
            instances.append(instance)

        return instances

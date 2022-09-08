from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
from collections.abc import Container
import importlib

T = TypeVar('T')





"""
A chave dos objetos do arquivo de configuração devem ser padronizadas
de forma com que eu consiga iterar sobre qualquer objeto de classe nessa
fábrica generica

"""


class AbstractEntityFactory(ABC, Generic[T]):

    @abstractmethod
    def create(self) -> T:
        pass


class GenericFactory(AbstractEntityFactory):
    def __init__(self, parameters: dict):
        self.parameters = self._handle_config_obj(parameters)

    def _handle_config_obj(self, parameters: dict) -> dict:
        """


        @type parameters: object
        @param config_obj:
        @return: object or None
        """

        visualizations = parameters['visualizations']

        is_empty = self._is_visualizations_empty(visualizations)
        if is_empty:
            raise Exception("Não foram inseridos estágios de pré-processamento, esse array não deve estar vazio")

        return parameters

    def _is_visualizations_empty(self, visualizations: list) -> bool:
        """
        Verifica se a lista de estágios de preprocessamento está vazia

        @param stages:
        @return:
        """
        if len(visualizations) == 0:
            return True

        return False

    @property

    def create(self):
        """


        @return: object
        """
        instances = []

        for stages in self.parameters['visualizations']:

            class_module = stages['module']
            class_name = stages['class_name']

            module = importlib.import_module(class_module)
            class_ = getattr(module, class_name)

            instance = class_(stages['parameters'])
            instances.append(instance)

        return instances

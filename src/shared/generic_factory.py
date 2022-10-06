from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List
import importlib
from src.utils import is_structure_empty

T = TypeVar('T')



class AbstractEntityFactory(ABC, Generic[T]):

    @abstractmethod
    def create(self) -> T:
        pass



#Condensar todas as factories aqui na generica.
class GenericFactory(AbstractEntityFactory):
    def __init__(self, parameters: dict):
        self.parameters = self._handle_config_obj(parameters)

    def _handle_config_obj(self, parameters: dict) -> dict:
        """


        @type parameters: object
        @param config_obj:
        @return: object or None
        """

        instances = parameters['instances']
        is_empty = is_structure_empty(instances)
        if is_empty:
            raise Exception("Não foram inseridos estágios de pré-processamento, esse array não deve estar vazio")

        return parameters


    @property
    def create(self):
        """


        @return: object
        """
        instances = [] #Poderia ser um dicionário -> Instancia e Nome da instancia

        for stages in self.parameters['instances']:

            class_module = stages['module']
            class_name = stages['class_name']

            module = importlib.import_module(class_module)
            class_ = getattr(module, class_name)

            instance = class_(stages['parameters'])
            instances.append(instance)

        return instances

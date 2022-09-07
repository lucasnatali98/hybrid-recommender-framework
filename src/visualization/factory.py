from abc import abstractmethod
from src.visualization.visualization import Visualization
import importlib


class Creator:

    @abstractmethod
    def create(self) -> Visualization:
        pass


class VisualizationFactory(Creator):
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
        Cria uma instância de um objeto do tipo PreProcessing

        @return: object
        """
        instances = []
        for stages in self.parameters['visualizations']:
            class_file = stages['class_file']
            module = importlib.import_module('src.visualization.' + class_file)
            class_ = getattr(module, stages['class_name'])
            instance = class_(stages['parameters'])
            instances.append(instance)

        return instances

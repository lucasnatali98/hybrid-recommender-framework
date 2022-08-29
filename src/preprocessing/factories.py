from abc import abstractmethod

from src.preprocessing.preprocessing import PreProcessing, AbstractPreProcessing
from src.preprocessing.encoding import EncodingProcessing
from src.preprocessing.split import SplitProcessing
from src.preprocessing.normalize import NormalizeProcessing
from src.preprocessing.discretize import DiscretizeProcessing

"""
1. Generalizar as fabricas em uma classe
"""


class Creator:

    @abstractmethod
    def create(self) -> AbstractPreProcessing:
        pass


class ProcessingFactory(Creator):
    def __init__(self, config_obj: dict):

        config_obj = self._handle_config_obj(config_obj)

        if not isinstance(config_obj, dict):
            print("Erro na definição do objeto de configuração")

        self.config_obj = config_obj

    def _handle_config_obj(self, config_obj: dict):
        """
        Tem como objetivo verificar a validade do arquivo de configuração para a execução
        das etapas de pré-processamento

        @param config_obj:
        @return: object or None
        """

        # Verificação das chaves pode ser um processo comum a todas as classes
        #
        config_keys = ["class", "module", "parameters"]
        has_config_keys = []

        for key in config_keys:
            if key in config_obj:
                has_config_keys.append(True)
            else:
                has_config_keys.append(False)

        if has_config_keys.index(False):
            raise Exception("Não existem todas as chaves necessárias para a execução do projeto")

        parameters = config_obj['parameters']
        stages = parameters['stages']

        is_empty = self._is_stages_empty(stages)
        if is_empty:
            raise Exception("Não foram inseridos estágios de pré-processamento, esse array não deve estar vazio")

        return config_obj

    def _is_stages_empty(self, stages):
        if len(stages) == 0:
            return True

        return False

    @property
    def create(self):
        """
        Cria uma instância de um objeto do tipo PreProcessing

        @return: object
        """

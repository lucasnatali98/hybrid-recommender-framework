from src.data import *
from src.preprocessing import *
from src.experiments import *
from src.metafeatures import *
from src.metrics import *
from src.recommenders import *
from src.results import *
from src.visualization import *
import importlib

"""

1. O intuito vai ser delegar a criação dos objetos para cada classe
2. InstanceFactory vai apenas gerenciar a conexão entre config.json e as classes. 
3. Achar uma forma de importar tudo que eu preciso de uma só vez.
4. Import dinamico
"""


class InstanceFactory:
    """
    A classe InstanceFactory é responsável por receber o arquivo de configuração

    """

    def __init__(self, config_obj=dict):
        """

        @param config_obj:
        """
        #self._handle_config_obj(config_obj)
        self.config_obj = config_obj

    def _handle_config_obj(self, config_obj: object):
        """

        @param config_obj:
        @return:
        """
        module = importlib.import_module(experiment['handler_module'])
        class_ = getattr(module, experiment['handler_name'])
        for key, value in config_obj.items():
            if value['class'] == "PreProcessingContainer":
                instance = self.create_instance(value)

    def get_instance_from_config_obj(self, class_name: str) -> dict:
        """
        Busca por uma instancia especifica dentro do objeto de configuração

        @param class_name:
        @return: um dicionário contendo informações para que seja criada a instância
        """
        for key, value in self.config_obj.items():
            if value['class'] == class_name:
                return value

    def create_instance(self, instance: dict):  # receber um dicionario
        """
        Essa função realiza a criação de uma instancia de uma classe de acordo com uma string informada


        @param instance: dicionário contendo informações para a criação da instancia

        @return: object


        """

        class_name = instance['class']
        module_name = instance['module']
        class_parameters = instance['parameters']

        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)

        try:
            return class_(class_parameters)
        except RuntimeError:
            raise Exception(f"[InstanceFactory.create_instance] <message_error>\n")



from src.data import *
from src.preprocessing import *
from src.experiments import *
from src.metafeatures import *
from src.metrics import *
from src.recommenders import *
from src.results import *
from src.visualization import *




"""

1. O intuito vai ser delegar a criação dos objetos para cada classe
2. InstanceFactory vai apenas gerenciar a conexão entre config.json e as classes. 
3. Achar uma forma de importar tudo que eu preciso de uma só vez.
4. Import dinamico
"""


class InstanceFactory:
    """
    A classe Reflection é responsável por instanciar diferentes objetos de nossa aplicação
    esses objetos são informados via arquivo de configuração.

    """

    def __init__(self, config_obj={}):
        """

        @param config_obj:
        """
        self._handle_config_obj(config_obj)
        self.config_obj = config_obj

    def _handle_config_obj(self, config_obj: object):
        """

        @param config_obj:
        @return:
        """

        for key, value in config_obj.items():
            if value['class'] == "PreProcessingContainer":
                instance = self.create_instance(value)

    def get_instance_from_config_obj(self, class_name: str) -> dict:
        """

        @param class_name:
        @return:
        """
        for key, value in self.config_obj.items():
            if value['class'] == class_name:
                return value

    def create_instance(self, instance: dict):  # receber um dicionario
        """
        Essa função realiza a criação de uma instancia de uma classe de acordo com uma string informada


        @param instance:

        @return: object


        """

        class_name = instance['class']
        class_parameters = instance['parameters']

        if self._check_valid_instance(class_name):
            try:
                return preprocessing_container.PreProcessingContainer(class_parameters['stages'])
            except:
                raise Exception(f"[InstanceFactory.create_instance] <message_error>\n")
        else:
            raise Exception(
                "[InstanceFactory.create_instance] the informed instance is invalid, define only an existing class in the global scope of the project")

    def _check_valid_instance(self, instance: str):
        """
        @param instance: str
        @return:

        """
        return True
        instance_class = globals()[instance]
        instance_class = instance_class()

        if instance_class:
            return True

        return False

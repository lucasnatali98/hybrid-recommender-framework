from src.experiments import *
import importlib
from src.preprocessing import *

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

        self.config_obj = config_obj


    def get_instance_from_config_obj(self, class_name: str) -> dict:
        """
        Busca por uma instancia especifica dentro do objeto de configuração

        @param class_name:
        @return: um dicionário contendo informações para que seja criada a instância
        """
        for key, value in self.config_obj.items():
            if value['class'] == class_name:
                return value

    def create_instance(self, instance: dict):
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

        class_object = class_(class_parameters)


        return class_object


from src.data.loader import Loader

from src.preprocessing import *

"""

1. O intuito vai ser delegar a criação dos objetos para cada classe
2. InstanceFactory vai apenas gerenciar a conexão entre config.json e as classes. 
3. Achar uma forma de importar tudo que eu preciso de uma só vez.

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
        self.config_obj = config_obj

    def _handle_config_obj(self, config_obj: object):
        """

        @param config_obj:
        @return:
        """

        pass


    def create_instance(self, instance: dict): #receber um dicionario
        """
        Essa função realiza a criação de uma instancia de uma classe de acordo com uma string informada


        @param instance:

        @return: object


        """

        #Colocar menção para o local do erro e exibição do stacktrace
        #Olhar se o erro tras todas informações que preciso ou se terei que definir explicitamente.

        class_name = instance['class']
        class_parameters = instance['parameters']
        if self._check_valid_instance(class_name):
            try:
                instance = globals()[class_name](class_parameters)
                return instance
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

        instance_class = globals()[instance]
        instance_class = instance_class()

        if instance_class:
            return True

        return False

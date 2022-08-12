from src.data.movielens import MovieLens
from src.data.loader import Loader
from src.data.movielens import MovieLens
from src.preprocessing.encoding import EncodingProcessing
from src.preprocessing.normalize import NormalizeProcessing
from src.preprocessing.split import SplitProcessing
from src.preprocessing.preprocessing import PreProcessingContainer


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


        """

        pass

    def create_all_instances(self, config_obj: object):
        """


        """
        for i in config_obj:
            print(i)

        instances = {}

    def create_instance(self, instance: str):
        """
        Essa função realiza a criação de uma instancia de uma classe de acordo com uma string informada


        @param instance:

        @return: object


        """

        if self._check_valid_instance(instance):
            instance = globals()[instance]()

            return instance

        raise Exception(
            "the informed instance is invalid, define only an existing class in the global scope of the project")

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

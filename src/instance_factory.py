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

    def __init__(self):
        pass

    def create_all_instances(self, config_obj: object):
        """


        """
        pass
    def create_instance(self, instance: str):
        """
        Essa função realiza a criação de uma instancia de uma classe de acordo com uma string informada

        @param instance: str

        :return
        """

        print(globals()[instance])

        if self._check_valid_instance(instance):
            instance = globals()[instance]('ml-latest-small')
            return instance

        raise Exception("A instancia informada não é válida")

    def _check_valid_instance(self, instance: str):
        """


        """

        instance_class = globals()[instance]
        instance_class = instance_class("ml-latest-small")



        return True

from src.metrics.metric import DiversityMetric
from src.utils import process_parameters
import pandas as pd

import jpype
import jpype.imports
from jpype.types import *

# Launch the JVM
jpype.startJVM(classpath=['/home/usuario/PycharmProjects/RecSysExp/src/jython/RankSys-diversity-0.4.3.jar'])

# import the Java modules
EILD = JClass('es.uam.eps.ir.ranksys.diversity.distance.metrics.EILD')
eild_instance = EILD()

class EILD(DiversityMetric):
    def __init__(self, parameters: dict) -> None:
        """

        """
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        raise NotImplementedError


class RankSysEILD(EILD):
    def __init__(self, parameters: dict) -> None:
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        return eild_instance.algumacoisa(predictions, truth)


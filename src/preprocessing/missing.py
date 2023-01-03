from src.preprocessing.preprocessing import AbstractPreProcessing
from src.utils import process_parameters, hrf_experiment_output_path

class MissingProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict):
        super().__init__()

        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def pre_processing(self, data, **kwargs):
        pass
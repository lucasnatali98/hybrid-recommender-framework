
from src.hybrid.hybrid_weighted import HybridWeighted
from src.utils import process_parameters


class STREAM(HybridWeighted):

    def __init__(self, parameters:dict) -> None:
        """
        
        """
        super().__init__()
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)



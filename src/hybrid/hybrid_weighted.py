from src.hybrid.hybrid import Hybrid
from src.utils import process_parameters


class HybridWeighted(Hybrid):
    def __init__(self, parameters: dict) -> None:
        super().__init__()
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

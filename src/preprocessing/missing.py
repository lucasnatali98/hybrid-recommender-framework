from src.preprocessing.preprocessing import AbstractPreProcessing
from src.utils import process_parameters, hrf_experiment_output_path
import pandas as pd

class MissingProcessing(AbstractPreProcessing):
    def __init__(self, parameters: dict):
        super().__init__()

        default_keys = set()
        parameters = process_parameters(parameters, default_keys)
        self.parameters = parameters
        self.preprocessing_output_dir = hrf_experiment_output_path().joinpath("preprocessing/")

    def check_missing_values(self, data: pd.DataFrame):
        pass

    def check_none(self, data: pd.DataFrame):
        item = data['item']
        rating = data['rating']
        user = data['user']

        item = list(filter(
            lambda x: x is None or x == "None",
            item
        ))
        user = list(filter(
            lambda x: x is None or x == "None",
            user
        ))
        rating = list(filter(
            lambda x: x is None or x == "None",
            rating
        ))

        if len(rating) == 0 and len(user) == 0 and len(item) == 0:
            print("Não existe nenhum valor None na base")
            return data
        else:
            print("")

    def pre_processing(self, data: pd.DataFrame, **kwargs) -> pd.DataFrame:
        print("missing processing")
        is_null = data.isnull().sum().values.any()
        is_na = data.isna().sum().values.any()
        print("Verifica is_null no dataframe: ", is_null)
        print("Verifica is_na no dataframe: ", is_na)
        data = self.check_none(data)

        if is_na is False and is_null is False:
            return data

        data.dropna(inplace=True)
        return data

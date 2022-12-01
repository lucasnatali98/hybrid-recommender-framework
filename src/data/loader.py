import pandas
import pandas as pd
import json
import pathlib
import os
from src.utils import get_project_root

ROOT_PATH = get_project_root()


class Loader:
    def __init__(self) -> None:
        """

        """
        pass



    def load_json_file(self, path):
        """

        """
        file = open(ROOT_PATH.joinpath(path))

        return json.load(file)


    def load_file(self, path, extension):
        """
        Carrega um arquivo baseado em sua extensão

        @path: path to file
        @extension: extension file

        """
        if extension == ".csv":
            return self.load_csv_file(path+extension)
        if extension == ".xls":
            return self.load_excel_file(path+extension)
        if extension == ".json":
            return self.load_json_file(path+extension)

        return False

    def load_csv_file(self, path):
        """

        """
        return pandas.read_csv(ROOT_PATH.joinpath(path))

    def load_excel_file(self, path):
        """

        """
        return pandas.read_excel(io=ROOT_PATH.joinpath(path))

    def convert_to(self, to, data, path):
        """

        """
        to_possibilities = ["csv", "excel"]

        if to in to_possibilities:
            if to == "csv":
                return self.convert_to_csv(data, path)
            if to == "excel":
                return self.convert_to_excel(data, path)

        return None

    def convert_to_csv(self, data, path):
        """
        Convert a dataframe to .csv file

        @data: pd.DataFrame

        """

        if isinstance(data, pandas.DataFrame):
            new_path = "data_storage/temp_files/" + path

            return data.to_csv(ROOT_PATH.joinpath(new_path))
        else:
            try:
                data = pd.DataFrame(data)
                new_path = "data_storage/temp_files/" + path
                return data.to_csv(ROOT_PATH.joinpath(new_path))
            except:
                raise Exception("Não foi possível gravar o arquivo .csv")

    def convert_to_excel(self, data, path):
        """
        Convert a dataframe to excel file


        """
        if isinstance(data, pandas.DataFrame):
            return data.to_excel()
        else:
            try:
                data = pd.DataFrame(data)
                new_path = "data_storage/temp_files/" + path
                return data.to_excel(ROOT_PATH.joinpath(new_path))
            except:
                raise Exception("Não foi possível converter para excel")

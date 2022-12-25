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

    def load_json_file(self, path: str):
        """

        @param path:
        @return:
        """
        file = open(ROOT_PATH.joinpath(path))

        return json.load(file)

    def load_file(self, path: str, extension: str):
        """
        Carrega um arquivo baseado em sua extensão

        @path: path to file
        @extension: extension file

        """
        if extension == ".csv":
            return self.load_csv_file(path + extension)
        if extension == ".xls":
            return self.load_excel_file(path + extension)
        if extension == ".json":
            return self.load_json_file(path + extension)

        return False

    def load_csv_file(self, path: str):
        """

        @param path: caminho do arquivo csv que será carregado
        @return:
        """
        return pandas.read_csv(ROOT_PATH.joinpath(path))

    def load_excel_file(self, path: str):
        """

        @param path: caminho do arquivo excel que será carregado
        @return:
        """
        return pandas.read_excel(io=ROOT_PATH.joinpath(path))

    def convert_to(self, to: str, data: pd.DataFrame, path: str):
        """

        Essa funçãoa faz a conversão de um dataframe em csv ou excel

        @param to: tipo de arquivo: csv ou excel
        @param data: dados a serem salvos: pd.DataFrame
        @param path: caminho onde o arquivo será salvo
        @return:
        """
        to_possibilities = ["csv", "excel"]

        if to in to_possibilities:
            if to == "csv":
                return self.convert_to_csv(data, path)
            if to == "excel":
                return self.convert_to_excel(data, path)

        return None

    def convert_to_csv(self, data: pd.DataFrame, path: str):
        """
        Converte um DataFrame do Pandas em um arquivo csv
        @param data: dataframe pandas
        @param path: caminho onde o csv será salvo
        @return:
        """

        if isinstance(data, pandas.DataFrame):
            new_path = path

            return data.to_csv(ROOT_PATH.joinpath(new_path))
        else:
            try:
                data = pd.DataFrame(data)
                new_path = path
                return data.to_csv(ROOT_PATH.joinpath(new_path))
            except:
                raise Exception("Não foi possível gravar o arquivo .csv")

    def convert_to_excel(self, data: pd.DataFrame, path: str):
        """
        Converte um DataFrame do Pandas em um arquivo excel
        @param data: dataframe pandas
        @param path: caminho onde o arquivo será salvo
        @return:
        """

        if isinstance(data, pandas.DataFrame):
            return data.to_excel()
        else:
            try:
                data = pd.DataFrame(data)
                new_path = "experiment_output/temp_files/" + path
                return data.to_excel(ROOT_PATH.joinpath(new_path))
            except:
                raise Exception("Não foi possível converter para excel")

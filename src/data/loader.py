import pandas
import pandas as pd
import json


class Loader:
    def __init__(self) -> None:
        """

        """

    def load_json_file(self, path):
        """

        """
        file = open(path)

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
        return pandas.read_csv(path)

    def load_excel_file(self, path):
        """

        """
        return pandas.read_excel(io=path)

    def convert_to(self, to, data):
        """

        """
        to_possibilities = ["csv", "excel"]

        if to in to_possibilities:
            if to == "csv":
                return self.convert_to_csv(data)
            if to == "excel":
                return self.convert_to_excel(data)

        return None

    def convert_to_csv(self, data):
        """
        Convert a dataframe to .csv file

        @data: pd.DataFrame

        """
        if isinstance(data, pandas.DataFrame):
            return data.to_csv()
        else:
            try:
                data = pd.DataFrame(data)
                return data.to_csv()
            except:
                raise Exception("Deu erro m")

    def convert_to_excel(self, data):
        """
        Convert a dataframe to excel file


        """
        if isinstance(data, pandas.DataFrame):
            return data.to_excel()
        else:
            try:
                data = pd.DataFrame(data)
                return data.to_excel()
            except:
                raise Exception("deu erro ai")

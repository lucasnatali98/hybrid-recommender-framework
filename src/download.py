from src.utils import hrf_data_storage_path
from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen


def download_and_unzip(url, extract_to):
    http_response = urlopen(url)

    zipfile = ZipFile(BytesIO(http_response.read()))

    zipfile.extractall(path=extract_to)

def download_database(database: str, proportion: str = ""):
    """

    @param database:
    @param proportion:
    @return:
    """
    pass
def download_movielens(proportion: str):
    """

    @param proportion:
    @return:
    """
    valid_proportions = {
        'ml-latest-small': "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip",
        'ml-latest': "https://files.grouplens.org/datasets/movielens/ml-latest.zip",
        'ml-25m': "https://files.grouplens.org/datasets/movielens/ml-25m.zip"
    }
    data_storage_path = str(hrf_data_storage_path())
    download_and_unzip(valid_proportions[proportion], data_storage_path)



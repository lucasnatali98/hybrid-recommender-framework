import yaml
import json
from src.data.loader import Loader



def json2yaml(file):
    """

    @param file:
    @return:
    """
    return yaml.dump(file, allow_unicode = True)

def yaml2json(file):
    """
    Essa função conver um arquivo yaml para um arquivo json

    @param file:arquivo no formato yaml
    @return: JSON
    """
    return json.dump(file)


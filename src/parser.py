import yaml
import json


def json2yaml(file: dict, stream):
    """


    @param file: dicionário com os dados
    @param stream: arquivo
    @return:
    """
    return yaml.dump(file, stream, allow_unicode = True)

def yaml2json(file):
    """
    Essa função conver um arquivo yaml para um arquivo json

    @param file:arquivo no formato yaml
    @return: JSON
    """
    return json.dump(file)


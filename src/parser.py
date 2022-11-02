import yaml
import json
from src.data.loader import Loader



def json2yaml(file):
    return yaml.dump(file, allow_unicode = True)

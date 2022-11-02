import yaml
import json
from src.data.loader import Loader

loader = Loader()

example_file = loader.load_json_file("src/example.json")

print(example_file)


def json2yaml(file):
    return yaml.dump(file, allow_unicode = True)

import json

import sys
import yaml
from pygments import highlight, lexers, formatters


def pretty_print(o):
    formatted_json = json.dumps(o, indent=2)
    colorful_json = highlight(formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter())
    print(colorful_json)


def load_yaml(path):
    with open(path, 'r') as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as e:
            print(e, file=sys.std err)

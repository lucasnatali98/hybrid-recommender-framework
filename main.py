
from src.experiments.experiment import ExperimentHandler


import json

"""
1. Focar no experimentor -> melhor desenvolver com ele desde o inicio (já testar com ele em bases pequenas)

2. É possível instanciar as classes a partir do arquivo de configuração
3. Próximo passo: Arquivo de configuração e documentação em paralelo com desenvolvimento
4. Design Patterns (criacionais para instanciar os objetos)
"""

file = open("config2.json")
config_obj = json.load(file)

experiments_config = config_obj['experiments']

print(experiments_config)

experiment_handler = ExperimentHandler()
instance = experiment_handler.create_experiment_instances(experiments_config)
print(instance)


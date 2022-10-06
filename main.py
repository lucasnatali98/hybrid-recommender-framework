
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



experiment_handler = ExperimentHandler()
instance = experiment_handler.create_experiment_instances(experiments_config)




dataset_instance = instance['datasets']
preprocessing_instance = instance['preprocessing']


after_filters = dataset_instance.apply_filters()
print("After filters:" , after_filters)

print("Ratings: ", dataset_instance.ratings)
"""
print("Tags: ", dataset_instance.tags)

print("Items (movies): ", dataset_instance.items)
print("Links: ", dataset_instance.links)
"""

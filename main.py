from src.instance_factory import InstanceFactory
import json


"""
1. Focar no experimentor -> melhor desenvolver com ele desde o inicio (já testar com ele em bases pequenas)

2. É possível instanciar as classes a partir do arquivo de configuração
3. Próximo passo: Arquivo de configuração e documentação em paralelo com desenvolvimento
4. Design Patterns (criacionais para instanciar os objetos)
"""

file = open("config.json")
config_obj = json.load(file)

instance_factory = InstanceFactory(config_obj)

instance_dict = instance_factory.get_instance_from_config_obj("PreProcessingContainer")
print(instance_dict)

instance = instance_factory.create_instance(instance_dict)
print(instance.print_instances())


from src.instance_factory import InstanceFactory
from src.preprocessing.encoding import EncodingProcessing
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

pre_processing_instance_dict = instance_factory.get_instance_from_config_obj("PreProcessingContainer")
#metrics_instance_dict = instance_factory.get_instance_from_config_obj("MetricsContainer")
#metafeatures_instance_dict = instance_factory.get_instance_from_config_obj("MetaFeatureContainer")
#recommenders_instance_dict = instance_factory.get_instance_from_config_obj("RecommendersContainer")
#visualization_instance_dict = instance_factory.get_instance_from_config_obj("VisualizationContainer")
#results_instance_dict = instance_factory.get_instance_from_config_obj("ResultsContainer")


preprocessing_instance = instance_factory.create_instance(pre_processing_instance_dict)
#metrics_instance = instance_factory.create_instance(metrics_instance_dict)
#metafeatures_instance = instance_factory.create_instance(metafeatures_instance_dict)
#recommenders_instance = instance_factory.create_instance(recommenders_instance_dict)

#visualization_instance = instance_factory.create_instance(visualization_instance_dict)
#results_instance = instance_factory.create_instance(results_instance_dict)




print(preprocessing_instance.print_instances())
#print(metrics_instance.print_instances())
#print(metafeatures_instance.print_instances())
#print(recommenders_instance.print_instances())
#print(visualization_instance.print_instances())
#print(results_instance.print_instances())

encoding = EncodingProcessing({
    "encoding_type": "onehot"
})



preprocessing_instance.push(encoding)

preprocessing_instance.print_instances()



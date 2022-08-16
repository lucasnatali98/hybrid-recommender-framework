from src.instance_factory import InstanceFactory
import json


"""
1. Focar no experimentor -> melhor desenvolver com ele desde o inicio (já testar com ele em bases pequenas)

2. É possível instanciar as classes a partir do arquivo de configuração
3. Próximo passo: Arquivo de configuração e documentação em paralelo com desenvolvimento
4. Design Patterns (criacionais para instanciar os objetos)
"""
"""


movie_lens_dataset = MovieLens("ml-latest-small")
pre_processing_container = PreProcessingContainer()
normalizer = NormalizeProcessing()
splitter = SplitProcessing()
ordinal = EncodingProcessing("onehot")

pre_processing_container.push(normalizer)
pre_processing_container.push(splitter)
pre_processing_container.push(ordinal)
pre_processing_container.print_instances()

X_train, X_test, y_train, y_test = splitter.pre_processing(movie_lens_dataset.tags)

# print(X_train)

tags = movie_lens_dataset.tags
tag = tags.tag
"""



object_factory = InstanceFactory()

loader = object_factory.create_instance("Loader")

config_obj = loader.load_file("config", ".json")



pre_processing_obj = config_obj['preprocessing']
print("PreProcessing Object: ", pre_processing_obj)


movie_lens = object_factory.create_instance("MovieLens")
split_processing = object_factory.create_instance("SplitProcessing")
normalize_processing = object_factory.create_instance("NormalizeProcessing")
encoding_processing = object_factory.create_instance("EncodingProcessing")
discretize_processing = object_factory.create_instance("DiscretizeProcessing")

pre_processing_instances = object_factory.create_pre_processing_instances(pre_processing_obj)
print("PreProcessing Instances: ", pre_processing_instances)
object_factory.create_all_instances(config_obj)

print(movie_lens.tags())
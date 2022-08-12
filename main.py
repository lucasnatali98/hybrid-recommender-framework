from src.instance_factory import InstanceFactory

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

movie_lens = object_factory.create_instance("MovieLens")
#split_processing = object_factory.create_instance("SplitProcessing")


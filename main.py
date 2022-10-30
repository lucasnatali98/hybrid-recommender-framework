
from src.experiments.experiment import ExperimentHandler

from external.deploy import DeployTest
import json

"""
1. Focar no experimentor -> melhor desenvolver com ele desde o inicio (já testar com ele em bases pequenas)

2. É possível instanciar as classes a partir do arquivo de configuração
3. Próximo passo: Arquivo de configuração e documentação em paralelo com desenvolvimento
4. Design Patterns (criacionais para instanciar os objetos)
"""
deploy = DeployTest()
deploy.deploy_in_cluster()


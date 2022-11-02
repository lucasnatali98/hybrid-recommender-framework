
from src.experiments.experiment import ExperimentHandler
from src.data.loader import Loader
from external.deploy import DeployTest, TaskExecutor, Xperimentor
from src.parser import json2yaml
import json

"""
1. Focar no experimentor -> melhor desenvolver com ele desde o inicio (já testar com ele em bases pequenas)

2. É possível instanciar as classes a partir do arquivo de configuração
3. Próximo passo: Arquivo de configuração e documentação em paralelo com desenvolvimento
4. Design Patterns (criacionais para instanciar os objetos)
"""


loader = Loader()

example_file = loader.load_json_file("src/example.json")

print(example_file)
output_file = json2yaml(example_file)
print("output file: ", output_file)
task_executor = TaskExecutor()
xperimentor = Xperimentor()
deploy_test = DeployTest()

deploy_test.deploy_in_cluster()

#task_executor_deploy_output = task_executor.deploy_in_cluster()
#xperimentor_deploy_output = xperimentor.deploy_in_cluster()

#print("Output - deploy task executor: ", task_executor_deploy_output)
#print("Output - deploy xperimentor: ", xperimentor_deploy_output)




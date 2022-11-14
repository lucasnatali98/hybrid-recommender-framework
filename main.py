from src.data.loader import Loader
from external.deploy import TaskExecutor, Xperimentor
from src.parser import json2yaml
import json
from src.data.data_handler import DataHandler
from src.experiments.experiment_handler import ExperimentHandler
from src.data.folds import Folds
"""
experiment_handler = ExperimentHandler(config_obj)

for exp in expeiment_handler.data:
    exp.run()

"""

"""
O que eu preciso fazer no mais alto nível da aplicação é organizar o
arquivo yaml na parte dos comandos com a execução de arquivos python
então teriamos vários processos de acordo com as etapas do arquivo de 
configuração.

"""

loader = Loader()
config_obj = loader.load_json_file("config.json")
experiments = config_obj['experiments']

experiment_handler = ExperimentHandler(experiments)
experiment_results = experiment_handler.run_experiments()
print("Experiment Results: ", experiment_results)


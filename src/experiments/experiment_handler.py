from src.experiments.experiment import AbstractExperiment, Experiment
from src.shared.container import Container
from typing import List
from src.data.loader import Loader


class ExperimentHandler(Container):
    def __init__(self, experiments=None, experiment_dependencies: dict = None, recipes_default: dict = None) -> None:
        """

        """
        super().__init__()

        if experiments is None:
            pass
        else:
            experiment = Experiment(
                experiment_obj=experiments[0],
                experiment_dependencies=experiment_dependencies,
                recipes_default=recipes_default

            )

            # Insere na estrutura de armazenamento dos experimentos
            self.items.append(experiment)

    def run_experiments(self) -> dict:
        result = {}
        print("Quantidade de experimentos que serão executados: ", len(self.items))
        for experiment in self.items:
            result[experiment.experiment_id] = experiment.run()

        return result

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass

    def create_experiment_instance(self):
        """
        Essa função cria uma instancia de um experimento a partir dos arquivos de configuração
        @return:
        """

        loader = Loader()

        config_obj = loader.load_json_file("config.json")
        experiments = config_obj['experiments']
        cluster_info = config_obj['cluster_info']
        recipes_default = config_obj['recipesDefault']
        experiment_dependencies = config_obj['experiment_dependencies']
        experiment = Experiment(
            experiment_obj=experiments[0],
            recipes_default=recipes_default,
            experiment_dependencies=experiment_dependencies
        )

        return experiment

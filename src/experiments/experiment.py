from src.instance_factory import InstanceFactory
from abc import ABC, abstractmethod
from external.deploy import Xperimentor, TaskExecutor
from src.parser import json2yaml, yaml2json
from src.data.loader import Loader
from src.tasks.task_factory import TaskFactory


class AbstractExperiment(ABC):

    @abstractmethod
    def run(self):
        """

        @return:
        """
        pass

    @abstractmethod
    def run(self):
        """

        @return:
        """
        pass


class Experiment(AbstractExperiment):
    """

        """

    experiment_id: str
    datasets: object
    preprocessing: object
    metrics: object
    metafeatures: object
    results: object
    visualization: object
    recommenders: object

    def __init__(self, experiment_obj: dict, experiment_dependencies: dict = None,
                 recipes_default: dict = None) -> None:
        """

        """

        # Informações provenientes do arquivo de configuração
        self.experiment_dependencies = experiment_dependencies
        self.recipes_default = recipes_default
        self.experiment_obj = experiment_obj
        self.experiment_id = experiment_obj['experiment_id']

        # Definição de todas as tarefas do framework (Executadas pelo Task Executor)
        self.task_factory = TaskFactory()
        self.tasks = self.define_all_tasks()

        # Definição de todas as instâncias baseado no experimento
        instances_obj = self.create_experiment_instances(experiment_obj)
        self._set_attributes(instances_obj)

        self.instances = None

    @property
    def experiment_obj(self):
        """
        Getter de experiment_obj

        @return: experiment_obj
        """
        return self.experiment_obj

    @property
    def experiment_dependencies(self):
        """

        @return:
        """
        return self.experiment_dependencies

    @property
    def recipes_default(self):
        """

        @return:
        """
        return self.recipes_default

    @recipes_default.setter
    def recipes_default(self, recipes):
        """

        @param recipes:
        @return:
        """
        self.recipes_default = recipes

    @experiment_dependencies.setter
    def experiment_dependencies(self, exp_dependencies):
        """

        @param exp_dependencies:
        @return:
        """
        self.experiment_dependencies = exp_dependencies

    @experiment_obj.setter
    def experiment_obj(self, exp_obj):
        """

        @param exp_obj:
        @return:
        """
        self.experiment_obj = exp_obj

    def define_all_tasks(self):
        """
        Cria um dicionário para mapear todas as tarefas

        @return: dict
        """
        tasks = {
            "dataset": self.task_factory.create("dataset"),
            "preprocessing": self.task_factory.create("preprocessing"),
            "algorithms": self.task_factory.create("algorithms"),
            "metrics": self.task_factory.create("metrics"),
            "results": self.task_factory.create("results"),
            "metafeatures": self.task_factory.create("metafeatures")
        }
        return tasks

    def run(self):
        """
        Função responsável pela execução do experimento.


        @return: Um arquivo YAML seguindo o padrão do Xperimentor
        """
        self.instances = self.create_experiment_instances(self.experiment_obj)

        xperimentor = Xperimentor()

        xperimentor_config_obj = xperimentor.convert_to_xperimentor_pattern(
            experiment_obj=self.experiment_obj,
            experiment_dependencies=self.experiment_dependencies
        )

        print("Xperimentor config obj")
        print(xperimentor_config_obj)

        loader = Loader()

        dataset = self.instances['datasets']
        preprocessing = self.instances['preprocessing']
        metafeatures = self.instances['metafeatures']
        recommenders = self.instances['recommenders']
        metrics = self.instances['metrics']
        results = self.instances['results']

        loader.convert_to("csv", dataset.ratings, "ratings.csv")

        # Todas as possíveis tarefas do framework
        dataset_task = self.tasks['dataset']
        preprocessing_task = self.tasks['preprocessing']
        algorithms_task = self.tasks['algorithms']
        metrics_task = self.tasks['metrics']
        results_task = self.tasks['results']
        metafeatures_task = self.tasks['metafeatures']

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass

    @property
    def datasets(self):
        return self.datasets

    @property
    def recommenders(self):
        return self.recommenders

    @property
    def preprocessing(self):
        return self.preprocessing

    @property
    def metrics(self):
        return self.metrics

    @property
    def results(self):
        return self.results

    def deploy_apps(self):
        task_executor = TaskExecutor()

        # Deploy do task executor no cluster Kubernetes
        # task_executor_output_build = task_executor.build()
        # task_executor_output_deploy = task_executor.deploy()

        # Deplou do task executor no cluster Kubernetes
        # xperimentor_output_build = xperimentor.build()
        # xperimentor_output_deploy = xperimentor.deploy()

    def _set_attributes(self, instances: dict):
        self.datasets = instances['datasets']
        self.metafeatures = instances['metafeatures']
        self.preprocessing = instances['preprocessing']
        self.results = instances['results']
        self.visualization = instances['visualization']
        self.recommenders = instances['recommenders']
        self.metrics = instances['metrics']

    def create_experiment_instances(self, config_obj) -> dict:
        """
        Faz a criação de todas as instâncias do programa utilizando do arquivo de configuração


        @param config_obj:
        @return: dict
        """

        instance_factory = InstanceFactory(config_obj)

        dataset_dict = instance_factory.get_instance_from_config_obj("MovieLens")

        pre_processing_instance_dict = instance_factory.get_instance_from_config_obj("PreProcessingContainer")

        metrics_instance_dict = instance_factory.get_instance_from_config_obj("MetricsContainer")
        metafeatures_instance_dict = instance_factory.get_instance_from_config_obj("MetaFeatureContainer")
        recommenders_instance_dict = instance_factory.get_instance_from_config_obj("RecommendersContainer")
        visualization_instance_dict = instance_factory.get_instance_from_config_obj("VisualizationContainer")
        results_instance_dict = instance_factory.get_instance_from_config_obj("ResultsContainer")

        dataset_instance = instance_factory.create_instance(dataset_dict)
        preprocessing_instance = instance_factory.create_instance(pre_processing_instance_dict)
        metrics_instance = instance_factory.create_instance(metrics_instance_dict)
        metafeatures_instance = instance_factory.create_instance(metafeatures_instance_dict)
        recommenders_instance = instance_factory.create_instance(recommenders_instance_dict)
        visualization_instance = instance_factory.create_instance(visualization_instance_dict)
        results_instance = instance_factory.create_instance(results_instance_dict)

        return {
            "datasets": dataset_instance,
            "preprocessing": preprocessing_instance,
            "metrics": metrics_instance,
            "metafeatures": metafeatures_instance,
            "visualization": visualization_instance,
            "recommenders": recommenders_instance,
            "results": results_instance
        }

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

    _experiment_id: str
    _datasets: object
    _preprocessing: object
    _metrics: object
    _metafeatures: object
    _results: object
    _visualization: object
    _recommenders: object

    def __init__(self, experiment_obj: dict, experiment_dependencies: dict = None,
                 recipes_default: dict = None) -> None:
        """

        """

        # Informações provenientes do arquivo de configuração
        self._experiment_dependencies = experiment_dependencies
        self._recipes_default = recipes_default
        self._experiment_obj = experiment_obj
        self._experiment_id = experiment_obj['experiment_id']

        # Definição de todas as tarefas do framework (Executadas pelo Task Executor)
        self._task_factory = TaskFactory()
        self._tasks = self.define_all_tasks()

        # Definição de todas as instâncias baseado no experimento
        instances_obj = self.create_experiment_instances(experiment_obj)
        self._set_attributes(instances_obj)

        self._instances = None

    @property
    def experiment_obj(self):
        """
        Getter de experiment_obj

        @return: experiment_obj
        """
        return self._experiment_obj

    @property
    def experiment_dependencies(self):
        """

        @return:
        """
        return self._experiment_dependencies

    @property
    def recipes_default(self):
        """

        @return:
        """
        return self._recipes_default

    @recipes_default.setter
    def recipes_default(self, recipes):
        """

        @param recipes:
        @return:
        """
        self._recipes_default = recipes

    @experiment_dependencies.setter
    def experiment_dependencies(self, exp_dependencies):
        """

        @param exp_dependencies:
        @return:
        """
        self._experiment_dependencies = exp_dependencies

    @experiment_obj.setter
    def experiment_obj(self, exp_obj):
        """

        @param exp_obj:
        @return:
        """
        self._experiment_obj = exp_obj

    def define_all_tasks(self):
        """
        Cria um dicionário para mapear todas as tarefas

        @return: dict
        """
        tasks = {
            "dataset": self._task_factory.create("dataset"),
            "preprocessing": self._task_factory.create("preprocessing"),
            "algorithms": self._task_factory.create("algorithms"),
            "metrics": self._task_factory.create("metrics"),
            "results": self._task_factory.create("results"),
            "metafeatures": self._task_factory.create("metafeatures")
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
            experiment_obj=self._experiment_obj,
            experiment_dependencies=self._experiment_dependencies
        )

        print("Xperimentor config obj")
        print(xperimentor_config_obj)

        loader = Loader()

        dataset = self._instances['datasets']
        preprocessing = self._instances['preprocessing']
        metafeatures = self._instances['metafeatures']
        recommenders = self._instances['recommenders']
        metrics = self._instances['metrics']
        results = self._instances['results']

        loader.convert_to("csv", dataset.ratings, "ratings.csv")

        # Todas as possíveis tarefas do framework
        dataset_task = self._tasks['dataset']
        preprocessing_task = self._tasks['preprocessing']
        algorithms_task = self._tasks['algorithms']
        metrics_task = self._tasks['metrics']
        results_task = self._tasks['results']
        metafeatures_task = self._tasks['metafeatures']

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass

    @property
    def datasets(self):
        return self._datasets

    @datasets.setter
    def datasets(self, ds):
        self._datasets = ds

    @property
    def recommenders(self):
        return self._recommenders

    @recommenders.setter
    def recommenders(self, rec):
        self._recommenders = rec

    @property
    def preprocessing(self):
        return self._preprocessing

    @preprocessing.setter
    def preprocessing(self, ps):
        self._preprocessing = ps

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, m):
        self._metrics = m

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, r):
        self._results = r

    @property
    def metafeatures(self):
        return self._metafeatures

    @metafeatures.setter
    def metafeatures(self, meta):
        self._metafeatures = meta

    @property
    def visualization(self):
        return self.visualization

    @visualization.setter
    def visualization(self, v):
        self._visualization = v

    def deploy_apps(self):
        task_executor = TaskExecutor()

        # Deploy do task executor no cluster Kubernetes
        # task_executor_output_build = task_executor.build()
        # task_executor_output_deploy = task_executor.deploy()

        # Deplou do task executor no cluster Kubernetes
        # xperimentor_output_build = xperimentor.build()
        # xperimentor_output_deploy = xperimentor.deploy()

    def _set_attributes(self, instances: dict):
        self._datasets = instances['datasets']
        self._metafeatures = instances['metafeatures']
        self._preprocessing = instances['preprocessing']
        self._results = instances['results']
        self._visualization = instances['visualization']
        self._recommenders = instances['recommenders']
        self._metrics = instances['metrics']

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

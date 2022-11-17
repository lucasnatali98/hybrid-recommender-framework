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

        self.experiment_dependencies = experiment_dependencies
        self.recipes_default = recipes_default
        self.config_obj = experiment_obj
        self.experiment_id = experiment_obj['experiment_id']
        instances_obj = self.create_experiment_instances(experiment_obj)
        self._set_attributes(instances_obj)
        self.task_factory = TaskFactory()
        self.tasks = self.define_all_tasks()

    def define_all_tasks(self):
        """

        @return:
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

        @return:
        """
        instances = self.create_experiment_instances(self.config_obj)

        xperimentor = Xperimentor()

        xperimentor_config_obj = xperimentor.convert_to_xperimentor_pattern(
            experiment_obj=self.config_obj,
            experiment_dependencies=self.experiment_dependencies
        )

        print("Xperimentor config obj")
        print(xperimentor_config_obj)

        dataset = instances['datasets']
        preprocessing = instances['preprocessing']
        metafeatures = instances['metafeatures']
        recommenders = instances['recommenders']
        metrics = instances['metrics']
        results = instances['results']

        #Todas as possíveis tarefas do framework
        dataset_task = self.tasks['dataset']
        preprocessing_task = self.tasks['preprocessing'](dataset, preprocessing)
        algorithms_task = self.tasks['algorithms']()
        metrics_task = self.tasks['metrics']()
        results_task = self.tasks['results']()
        metafeatures_task = self.tasks['metafeatures'](dataset)

        preprocessing = preprocessing_task.run()
        dataset = dataset_task.run()
        metrics = metrics_task.run()
        metafeatures = metafeatures_task.run()
        recommenders = algorithms_task.run()
        results = results_task.run()




    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass

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



        @param config_obj:
        @return:
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

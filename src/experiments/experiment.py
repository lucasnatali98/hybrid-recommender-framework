from dataclasses import dataclass
from src.experiments.experiment import Experiment
from src.instance_factory import InstanceFactory
from abc import ABC, abstractmethod
from external.deploy import Xperimentor, TaskExecutor
from src.utils import subprocess_output_is_correct

class AbstractExperiment(ABC):

    @abstractmethod
    def run(self):
        """

        @return:
        """
        pass

    @abstractmethod
    def set_experiment(self, experiment: dict):
        """

        @param experiments:
        @return:
        """
        pass


class Experiment:
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

    def __init__(self) -> None:
        """

        """
        self.experiments = []

    def run(self):
        """

        @return:
        """

        # config_file_yaml = json2yaml(config_obj)
        xperimentor = Xperimentor()
        xperimentor.convert_to_xperimentor_pattern(config_obj={})

        task_executor = TaskExecutor()

        #Deploy do task executor no cluster Kubernetes
        task_executor_output_build = task_executor.build()
        task_executor_output_deploy = task_executor.deploy()

        #Deplou do task executor no cluster Kubernetes
        xperimentor_output_build = xperimentor.build()
        xperimentor_output_deploy = xperimentor.deploy()




    def __str__(self):
        print(
            "Descrição do experimento: \n",
            "Nome do experimento: ", self.experiment_id,
        )

    def _handle_with_dataset(self, dataset):
        pass

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
        instance_factory = InstanceFactory(config_obj[0])

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

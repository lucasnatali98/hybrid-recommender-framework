from dataclasses import dataclass
from abc import ABC, abstractmethod
from src.instance_factory import InstanceFactory


class Experiment(ABC):


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

    @abstractmethod
    def add(self, experiment):
        """

        @param experiment:
        @return:
        """
        pass

    @abstractmethod
    def insert(self, experiments):
        """

        @param experiments:
        @return:
        """
        pass

    @abstractmethod
    def remove(self, experiment):
        """

        @param experiment:
        @return:
        """
        pass

    @abstractmethod
    def removeAll(self):
        """

        @return:
        """
        pass




@dataclass
class ExperimentHandler(Experiment):
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
        pass


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

    def set_experiment(self, experiment: dict) -> None:
        """

        @param experiments:
        @return:
        """

        if bool(experiment) == False:
            print("Experiment object is empty")


        self.experiments.append(experiment)


    def add(self, experiment) -> None:
        """

        @param experiment:
        @return:
        """
        pass

    def insert(self, experiments) -> None:
        """

        @param experiments:
        @return:
        """
        pass

    def remove(self, experiment) -> None:

        """

        @param experiment: dict
        @return:
        """
        self.experiments.remove(experiment)

    def removeAll(self) -> None:
        """

        @return:
        """
        self.experiments.clear()

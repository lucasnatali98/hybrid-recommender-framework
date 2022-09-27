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
    def set_experiments(self, experiments):
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

    def __init__(self):
        """
        
        """
        self.experiments = []

    def run(self):
        """

        @return:
        """
        pass

    def create_experiment_instances(self, config_obj):

        """



        @param config_obj:
        @return:
        """
        instance_factory = InstanceFactory(config_obj[0])

        pre_processing_instance_dict = instance_factory.get_instance_from_config_obj("PreProcessingContainer")

        metrics_instance_dict = instance_factory.get_instance_from_config_obj("MetricsContainer")
        metafeatures_instance_dict = instance_factory.get_instance_from_config_obj("MetaFeatureContainer")
        recommenders_instance_dict = instance_factory.get_instance_from_config_obj("RecommendersContainer")
        visualization_instance_dict = instance_factory.get_instance_from_config_obj("VisualizationContainer")
        results_instance_dict = instance_factory.get_instance_from_config_obj("ResultsContainer")

        preprocessing_instance = instance_factory.create_instance(pre_processing_instance_dict)
        metrics_instance = instance_factory.create_instance(metrics_instance_dict)
        metafeatures_instance = instance_factory.create_instance(metafeatures_instance_dict)
        recommenders_instance = instance_factory.create_instance(recommenders_instance_dict)
        visualization_instance = instance_factory.create_instance(visualization_instance_dict)
        results_instance = instance_factory.create_instance(results_instance_dict)

        return {
            "preprocessing": preprocessing_instance,
            "metrics": metrics_instance,
            "metafeatures": metafeatures_instance,
            "visualization": visualization_instance,
            "recommenders": recommenders_instance,
            "results": results_instance
        }

    def set_experiments(self, experiments):
        """

        @param experiments:
        @return:
        """


        pass


    def add(self, experiment):
        """

        @param experiment:
        @return:
        """
        pass

    def insert(self, experiments):
        """

        @param experiments:
        @return:
        """
        pass

    def remove(self, experiment):
        """

        @param experiment:
        @return:
        """
        pass

    def removeAll(self):
        """

        @return:
        """
        pass

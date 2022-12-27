from src.instance_factory import InstanceFactory
from abc import ABC, abstractmethod
from external.deploy import Xperimentor, TaskExecutor
from src.parser import json2yaml, yaml2json
from src.data.loader import Loader
from src.tasks.task_factory import TaskFactory
from src.utils import hrf_task_path, get_project_root, process_parameters


class AbstractExperiment(ABC):
    """
    Interface para os experimentos
    """

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
    def __init__(self, experiment: dict) -> None:
        default_keys = {
            'dataset',
            'preprocessing',
            'metrics',
            'recommenders',
            'results',
            'visualization',
            'metafeatures'
        }
        experiment = process_parameters(experiment, default_keys)
        self._experiment = experiment
        self._experiment_id = self._experiment.get('experiment_id')


        # Definição de todas as instâncias baseado no experimento
        instances_obj = self.create_experiment_instances(experiment)
        self._set_attributes(instances_obj)
        self._instances = instances_obj

    @property
    def instances(self) -> dict:
        return self._instances



    def run(self):
        """
        Função responsável pela execução do experimento.


        @return: Um arquivo YAML seguindo o padrão do Xperimentor
        """
        self._instances = self.create_experiment_instances(self._experiment)
        return self._instances


    def _set_attributes(self, instances: dict):
        self._datasets = instances['datasets']
        self._metafeatures = instances['metafeatures']
        self._preprocessing = instances['preprocessing']
        self._results = instances['results']
        self._visualization = instances['visualization']
        self._recommenders = instances['recommenders']
        self._metrics = instances['metrics']


    def create_experiment_instances(self, experiment: dict) -> dict:
        """
        Faz a criação de todas as instâncias do programa utilizando do arquivo de configuração


        @param config_obj:
        @return: dict
        """

        instance_factory = InstanceFactory(experiment)

        dataset_class_name = experiment['dataset']['class']
        preprocessing_class_name = experiment['preprocessing']['class']
        metrics_class_name = experiment['metrics']['class']
        metafeatures_class_name = experiment['metafeatures']['class']
        recommenders_class_name = experiment['recommenders']['class']
        visualization_class_name = experiment['visualization']['class']
        results_class_name = experiment['results']['class']

        dataset_object = instance_factory.get_instance_from_config_obj(dataset_class_name)
        preprocessing_object = instance_factory.get_instance_from_config_obj(preprocessing_class_name)
        metafeatures_object = instance_factory.get_instance_from_config_obj(metafeatures_class_name)
        recommenders_object = instance_factory.get_instance_from_config_obj(recommenders_class_name)
        visualization_object = instance_factory.get_instance_from_config_obj(visualization_class_name)
        results_object = instance_factory.get_instance_from_config_obj(results_class_name)
        metrics_object = instance_factory.get_instance_from_config_obj(metrics_class_name)

        dataset_instance = instance_factory.create_instance(dataset_object)
        preprocessing_instance = instance_factory.create_instance(preprocessing_object)
        metafeatures_instance = instance_factory.create_instance(metafeatures_object)
        recommenders_instance = instance_factory.create_instance(recommenders_object)
        visualization_instance = instance_factory.create_instance(visualization_object)
        results_instance = instance_factory.create_instance(results_object)
        metrics_instance = instance_factory.create_instance(metrics_object)

        return {
            "datasets": dataset_instance,
            "preprocessing": preprocessing_instance,
            "metafeatures": metafeatures_instance,
            "recommenders": recommenders_instance,
            "results": results_instance,
            "metrics": metrics_instance,
            "visualization": visualization_instance
        }

    @property
    def experiment_obj(self):
        return self._experiment_obj

    @property
    def experiment_id(self):
        return self._experiment_id
    @property
    def experiment_dependencies(self):
        return self._experiment_dependencie

    @property
    def recipes_default(self):
        return self._recipes_default

    @recipes_default.setter
    def recipes_default(self, recipes: dict):
        self._recipes_default = recipes

    @experiment_dependencies.setter
    def experiment_dependencies(self, exp_dependencie: dict):
        self._experiment_dependencie = exp_dependencie

    @experiment_obj.setter
    def experiment_obj(self, exp_obj: dict):
        self._experiment_obj = exp_obj

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



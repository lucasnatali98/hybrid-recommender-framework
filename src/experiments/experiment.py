from src.instance_factory import InstanceFactory
from abc import ABC, abstractmethod
from external.deploy import Xperimentor, TaskExecutor
from src.parser import json2yaml, yaml2json
from src.data.loader import Loader
from src.tasks.task_factory import TaskFactory


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
    _experiments: list

    def __init__(self, experiments: list, experiment_dependencies: dict = None,
                 recipes_default: dict = None, cluster_info: dict = None) -> None:
        """

        """

        #Informação do cluster
        print(cluster_info)
        self.cluster_info = cluster_info
        self.cluster_ip = self.cluster_info['clusterIp']
        self.cluster_name = self.cluster_info['clusterName']
        self.project_id = self.cluster_info['projectID']


        # Informações provenientes do arquivo de configuração
        self._experiment_dependencies = experiment_dependencies
        self._recipes_default = recipes_default
        self._experiments = experiments

        # Definição de todas as tarefas do framework (Executadas pelo Task Executor)
        self._task_factory = TaskFactory()
        self._tasks = self.define_all_tasks()

        # Definição de todas as instâncias baseado no experimento
        instances_obj = self.create_experiment_instances(experiments)
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
        tasks = {}
        exp_id = None
        default_tasks = [
            'dataset',
            'preprocessing',
            'metrics',
            'metafeatures',
            'recommenders',
            'visualization',
            'results'
        ]
        for exp in self._experiments:
            exp_keys = list(exp.keys())
            exp_keys = list(filter(lambda x: x in default_tasks, exp_keys))
            print(exp_keys)
            exp_id = exp['experiment_id']
            tasks.update({exp_id: {}})
            for task in default_tasks:
                tasks[exp_id].update({task: self._task_factory.create(task)})




        return tasks

    def run(self):
        """
        Função responsável pela execução do experimento.


        @return: Um arquivo YAML seguindo o padrão do Xperimentor
        """
        self._instances = self.create_experiment_instances(self._experiments)

        xperimentor = Xperimentor()

        xperimentor_config_obj = xperimentor.convert_to_xperimentor_pattern(
            experiments=self._experiments,
            experiment_dependencies=self._experiment_dependencies,
            recipes_default=self._recipes_default
        )

        print("Xperimentor config obj")
        print(xperimentor_config_obj)

        loader = Loader()



    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """

        pass

    @property
    def datasets(self):
        """

        @return:
        """
        return self._datasets

    @datasets.setter
    def datasets(self, ds):
        """

        @param ds:
        @return:
        """
        self._datasets = ds

    @property
    def recommenders(self):
        """

        @return:
        """
        return self._recommenders

    @recommenders.setter
    def recommenders(self, rec):
        """

        @param rec:
        @return:
        """
        self._recommenders = rec

    @property
    def preprocessing(self):
        """

        @return:
        """
        return self._preprocessing

    @preprocessing.setter
    def preprocessing(self, ps):
        """

        @param ps:
        @return:
        """
        self._preprocessing = ps

    @property
    def metrics(self):
        """

        @return:
        """
        return self._metrics

    @metrics.setter
    def metrics(self, m):
        """

        @param m:
        @return:
        """
        self._metrics = m

    @property
    def results(self):
        """

        @return:
        """
        return self._results

    @results.setter
    def results(self, r):
        """

        @param r:
        @return:
        """
        self._results = r

    @property
    def metafeatures(self):
        """

        @return:
        """
        return self._metafeatures

    @metafeatures.setter
    def metafeatures(self, meta):
        """

        @param meta:
        @return:
        """
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

    def _set_attributes(self, instances: list):

        instances = instances[0]['exp1']
        print("Instances: ", instances)
        self._datasets = instances['datasets']
        self._metafeatures = instances['metafeatures']
        self._preprocessing = instances['preprocessing']
        self._results = instances['results']
        self._visualization = instances['visualization']
        self._recommenders = instances['recommenders']
        self._metrics = instances['metrics']

    def create_experiment_instances(self, experiments) -> list:
        """
        Faz a criação de todas as instâncias do programa utilizando do arquivo de configuração


        @param config_obj:
        @return: dict
        """
        instances = []
        for experiment in experiments:
            instance_factory = InstanceFactory(experiment)

            dataset_class_name = experiment['dataset']['class']
            preprocessing_class_name = experiment['preprocessing']['class']
            metrics_class_name = experiment['metrics']['class']
            metafeatures_class_name = experiment['metafeatures']['class']
            recommenders_class_name = experiment['recommenders']['class']
            visualization_class_name = experiment['visualization']['class']
            results_class_name = experiment['results']['class']

            experiment_id = experiment['experiment_id']
            print("experiment id: ", experiment_id)

            experiment_classes = {
                "dataset": dataset_class_name,
                "preprocessing": preprocessing_class_name,
                "metefeatures": metafeatures_class_name,
                "metrics_class_name": metrics_class_name,
                "recommenders_class_name": recommenders_class_name,
                "visualization_class_name": visualization_class_name,
                "results_class_name": results_class_name
            }

            for key, value in experiment_classes.items():
                instance = instance_factory.get_instance_from_config_obj(value)
                dataset_instance = None
                preprocessing_instance = None
                metrics_instance = None
                metafeatures_instance = None
                visualization_instance = None
                recommenders_instance = None
                results_instance = None

                if key == "dataset":
                    dataset_instance = instance_factory.create_instance(instance)
                if key == "preprocessing":
                    preprocessing_instance = instance_factory.create_instance(instance)
                if key == "metrics":
                    metrics_instance = instance_factory.create_instance(instance)
                if key == "metafeatures":
                    metafeatures_instance = instance_factory.create_instance(instance)
                if key == "visualization":
                    visualization_instance = instance_factory.create_instance(instance)
                if key == "recommenders":
                    recommenders_instance = instance_factory.create_instance(instance)
                if key == "results":
                    results_instance = instance_factory.create_instance(instance)

                exp_obj = {}
                exp_obj[experiment_id] = {
                    "datasets": dataset_instance,
                    "preprocessing": preprocessing_instance,
                    "metrics": metrics_instance,
                    "metafeatures": metafeatures_instance,
                    "visualization": visualization_instance,
                    "recommenders": recommenders_instance,
                    "results": results_instance
                }
                instances.append(exp_obj)

        return instances

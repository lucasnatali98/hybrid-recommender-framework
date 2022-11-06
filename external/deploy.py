import subprocess
from abc import ABC, abstractmethod
from src.utils import subprocess_output_is_correct
from src.data.loader import Loader
class Xperimentor:
    def __init__(self):
        pass

    def convert_to_xperimentor_pattern(self, experiment_obj: dict):
        """

        @return:
        """
        loader = Loader()
        dataset = experiment_obj['datasets']
        metafeatures = experiment_obj['metafeatures']
        hybrid = None
        folds = None
        recommenders = experiment_obj['recommenders']
        metrics = experiment_obj['metrics']
        results = experiment_obj['results']


        # Preciso ter a relação dos folds -> Os datasets precisam guardar essa informação após gera-los
        xperimentor_pattern_obj = loader.load_json_file("external/xperimentor_config_file_pattern.json")
        xperimentor_pattern_obj['recipeDefaults']['DB'] = self._set_database_recipes(dataset)
        xperimentor_pattern_obj['recipeDefaults']['Fold'] = self._set_folds_recipes(folds)
        xperimentor_pattern_obj['recipeDefaults']['MF'] = self._set_metafeatures_recipes(metafeatures)
        xperimentor_pattern_obj['recipeDefaults']['Alg'] = self._set_algorithms_recipes(recommenders)
        xperimentor_pattern_obj['recipeDefaults']['HF'] = self._set_hybrid_recipes(hybrid)
        xperimentor_pattern_obj['recipeDefaults']['Eval'] = self._set_eval_recipes(metrics)
        xperimentor_pattern_obj['recipeDefaults']['Stats'] = self._set_stats_recipes(results)




        xperimentor_pattern_obj['recipes'][0]['uses']['DB'] = self._set_database_recipes(dataset)
        xperimentor_pattern_obj['recipes'][0]['uses']['Fold'] = self._set_folds_recipes(folds)
        xperimentor_pattern_obj['recipes'][0]['uses']['MF'] = self._set_metafeatures_recipes(metafeatures)
        xperimentor_pattern_obj['recipes'][0]['uses']['Alg'] = self._set_algorithms_recipes(recommenders)
        xperimentor_pattern_obj['recipes'][0]['uses']['HF'] = self._set_hybrid_recipes(hybrid)
        xperimentor_pattern_obj['recipes'][0]['uses']['Eval'] = self._set_eval_recipes(metrics)
        xperimentor_pattern_obj['recipes'][0]['uses']['Stats'] = self._set_stats_recipes(results)


        print("xperimentor_pattern_obj: ", xperimentor_pattern_obj)
        return xperimentor_pattern_obj

    def _set_database_recipes(self, database: dict) -> list:
        return [database['class']]

    def _set_hybrid_recipes(self, hybrid) -> list:
        return self._get_class_name_from_instance(hybrid)

    def _set_stats_recipes(self, results: dict) -> list:
        return self._get_class_name_from_instance(results)

    def _get_class_name_from_instance(self, obj: dict) -> list:
        """

        @param obj:
        @return: list
        """
        if obj is None:
            return []

        parameters = obj['parameters']
        instances = parameters['instances']
        return list(map(lambda x: x['class_name'], instances))
    def _set_folds_recipes(self, folds) -> list:
        return self._get_class_name_from_instance(folds)

    def _set_metafeatures_recipes(self, metafeatures: dict) -> list:
        return self._get_class_name_from_instance(metafeatures)

    def _set_algorithms_recipes(self, algorithms: dict) -> list:
        return self._get_class_name_from_instance(algorithms)

    def _set_eval_recipes(self, metrics: dict) -> list:
        return self._get_class_name_from_instance(metrics)

    def build(self):
        """

        @return:
        """
        output = subprocess.run(['sh, external/xperimentor/build.sh'], capture_output=True)

        if subprocess_output_is_correct(output) == True:
            print("O processo de build foi bem sucedido")

        raise Exception("Não foi possível construir a imagem")

    def deploy(self):
        output = subprocess.run(['sh', "external/xperimentor/deploy.sh"], capture_output=True)
        print("-- deploy Xperimentor by shell script file -- ")
        print("output: ", output)
        if subprocess_output_is_correct(output) == True:
           print("O deploy do Xperimentor ocorreu corretamente no cluster")

        raise Exception("Nao foi possível fazer o deploy do Xperimentor")

class TaskExecutor:
    def __init__(self):
        pass

    def build(self):
        """

        @return:
        """
        output = subprocess.run(['sh', "external/task-executor/build.sh"])
        print("-- Building Task Executor by shell script file -- ")
        if subprocess_output_is_correct(output) == True:
            print("The image was built successfully")
            print("Task Executor Build Output: ", output)
        else:
            print("Could not build image")
            print("Task Executor Build Output: ", output)
        return output
    def deploy(self):
        """

        @return:
        """
        output = subprocess.run(['sh', "external/task-executor/deploy.sh"])
        print("-- deploy Task Executor by shell script file -- ")

        if subprocess_output_is_correct(output) == True:
            print("The image was built successfully")
            print("Task Executor Deploy Output: ", output)
        else:
            print("Could not build image")
            print("Task Executor Deploy Output: ", output)

        return output

import sys
import subprocess
from src.data.loader import Loader
from src.tasks.task import Task


class PreProcessingTask(Task):
    def __init__(self, args):
        self.dataset = args

    def check_args(self, args):
        """

        @param args:
        @return:
        """
        pass

    def run(self):
        """

        @return:
        """
        pass
        #self._handle_pre_processing_tasks(self.dataset, self.preprocessing)


    def _handle_pre_processing_tasks(self, dataset, preprocessing):
        """

        @param dataset:
        @param preprocessing:
        @return:
        """
        execution_steps = {}
        items = preprocessing.items[0]
        for item in items:
            class_name = item.__class__.__name__
            result = item.pre_processing(dataset)
            execution_steps[class_name] = result

        self._save_splited_dataset(execution_steps['SplitProcessing'])
        print("=> Todas as tarefas de pré-processamento foram realizadas e salvas em diretórios temporários\n")

    def _save_splited_dataset(self, split_processing: dict):
        """

        @param split_processing:
        @return:
        """
        loader = Loader()
        for key, value in split_processing.items():
            if key == 'x_train':
                loader.convert_to("csv", value, "xtrain.csv")
            if key == 'x_test':
                loader.convert_to("csv", value, "xtest.csv")
            if key == 'y_train':
                loader.convert_to("csv", value, "ytrain.csv")
            if key == 'y_test':
                loader.convert_to("csv", value, 'ytest.csv')

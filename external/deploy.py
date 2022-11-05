import subprocess
from abc import ABC, abstractmethod
from src.utils import subprocess_output_is_correct

class Xperimentor:
    def __init__(self):
        pass

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

        pass
    def deploy(self):
        output = subprocess.run(['sh', "external/task-executor/deploy.sh"])
        print("-- deploy Task Executor by shell script file -- ")
        print("output: ", output)
        return output

class DeployTest:
    def __init__(self):
        pass

    def deploy_in_cluster(self):
        output = subprocess.run(['sh', 'external/example.sh'], capture_output=True)
        is_output_correct = subprocess_output_is_correct(output)
        print("is_output_correct: ", is_output_correct)
        print("output: ", output)
        if is_output_correct:
            print("O deploy ocorreu de forma bem sucedida")
        else:
            print("Houve um problema no deploy")



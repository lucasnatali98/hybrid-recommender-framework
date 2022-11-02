import subprocess
from abc import ABC, abstractmethod
from src.utils import subprocess_output_is_correct

class Xperimentor:
    def __init(self):
        pass

    def deploy_in_cluster(self):
        output = subprocess.run(['sh', "external/xperimentor/deploy.sh"])
        print("-- deploy Xperimentor by shell script file -- ")
        print("output: ", output)
        return output

class TaskExecutor:
    def __init__(self):
        pass

    def deploy_in_cluster(self):
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


class Deploy(ABC):
    @abstractmethod
    def deploy_in_cluster(self):
        pass


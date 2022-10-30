import subprocess
from abc import ABC, abstractmethod


class Xperimentor:
    def __init(self):
        pass

    def deploy_in_cluster(self):
        subprocess.run(['sh', "external/xperimentor/deploy.sh"])
        pass

class TaskExecutor:
    def __init__(self):
        pass

    def deploy_in_cluster(self):
        subprocess.run(['sh', 'external/task-executor/deploy.sh'])
        pass

class DeployTest:
    def __init__(self):
        pass

    def deploy_in_cluster(self):
        output = subprocess.run(['sh', 'external/example.sh'], capture_output=True)
        print(output)

class Deploy(ABC):
    @abstractmethod
    def deploy_in_cluster(self):
        pass


import subprocess
class TaskExecutor:
    def __init__(self):
        pass

    def build_task_executor(self):
        """

        @return:
        """

        output = subprocess.run(['sh', 'external/task-executor/build_image.sh'], capture_output=True)
        return output

    def deploy_task_executor(self):
        """

        @return:
        """
        output = subprocess.run(['sh', 'external/task-executor/deploy.sh'], capture_output=True)
        return output
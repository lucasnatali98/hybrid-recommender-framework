from src.utils import get_project_root
def hrf_task_path():
    """

    @return: Path to tasks
    """
    root_path = get_project_root()
    root_path = root_path.joinpath("tasks/")
    return root_path


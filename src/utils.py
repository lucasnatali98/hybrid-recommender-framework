from pathlib import Path

def object_equals_type(obj, object_type):
    """

    @param obj:
    @param object_type:
    @return:
    """
    if type(obj) is object_type:
        return True

    return False

def subprocess_output_is_correct(output):
    """
    Função responsável por verificar se a saída de CompletedProcess
    é correta ou não

    @param output:
    @return:
    """

    if output.returncode == 0:
        return True

    return False
def is_structure_empty(structure):
    """
    Essa função faz a verificação se uma determinada estrutura está vazia


    @param structure: estrutura iteravel
    @return: True ou False
    """
    if len(structure) == 0:
        return True

    return False


def get_project_root() -> Path:
    root_path = Path(__file__).parent.parent
    return root_path


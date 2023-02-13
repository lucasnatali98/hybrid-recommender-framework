from __future__ import annotations
from pathlib import Path
from pandas import DataFrame, Series
import os


def create_directory(path: Path, dir_name: str):
    """
    Função para criar um novo diretório no projetp
    @param path: Caminho base para criar o diretório
    @param dir_name: nome do diretório a ser criado
    @return: None or str
    """
    dir_path = path.joinpath(dir_name)
    directory_exists = check_if_directory_exists(dir_path)
    if directory_exists:
        return None
    else:
        os.makedirs(dir_path)
        return dir_path
def check_if_directory_exists(dir: Path):
    """
    Função para checar se o diretório existe
    @param dir: string para o caminho do diretório
    @return: bool -> Verdadeiro ou falso
    """
    return os.path.exists(dir)

def process_parameters(parameters: dict, default_keys: set) -> dict:
    parameters = convert_json_attribute_values_to_python(parameters)
    parameters_keys_list = list(parameters.keys())

    parameters_keys = set()

    for parameter in parameters_keys_list:
        parameters_keys.add(parameter)

    if default_keys.issubset(parameters_keys):
        pass
    else:
        raise KeyError("Você não informou uma das chaves obrigatorias: ", default_keys)
    return parameters


def convert_json_attribute_values_to_python(parameters: dict) -> dict:
    new_parameters = {}
    for key, value in parameters.items():
        if isinstance(value, DataFrame):
            new_parameters[key] = value
        elif isinstance(value, Series):
            new_parameters[key] = value
        elif value == "None":
            new_parameters[key] = None
        elif value == "true":
            new_parameters[key] = True
        elif value == "false":
            new_parameters[key] = False
        else:
            new_parameters[key] = value

    return new_parameters


def beautify_subprocess_output_response(output):
    if output == 1:
        return "Concluído com erros na execução"
    else:
        return "Concluído com sucesso"



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
    """
    Função para retornar o caminho para o diretório root da aplicação

    @return: Path: <your_local_path_to_hybrid_recommender_framework>
    """
    root_path = Path(__file__).parent.parent
    return root_path


def hrf_task_path():
    """
    Função responsável por gerar o path para a pasta de tarefas do projeto,
    o resultado dessa função será usada para criar os commandos do xperimentor

    @return: Path to tasks
    """
    root_path = get_project_root()
    root_path = root_path.joinpath("src/tasks/")
    return root_path


def hrf_experiment_output_path():
    """
    Função responsável por retornar o path para o diretório "experiment_output/"
    @return:
    """
    root_path = get_project_root()
    root_path = root_path.joinpath("experiment_output")
    return root_path

def hrf_external_path():
    """
    Função responsável por retornar o path para o diretório "external"

    @return: path
    """
    root_path = get_project_root()
    root_path = root_path.joinpath("external")
    return root_path
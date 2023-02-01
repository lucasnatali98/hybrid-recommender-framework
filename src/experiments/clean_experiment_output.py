from __future__ import annotations

import os
import shutil

from src.utils import hrf_experiment_output_path

folders = {
    "models": {
        "predictions": hrf_experiment_output_path().joinpath("models/results/predictions/"),
        "rankings": hrf_experiment_output_path().joinpath("models/results/rankings/"),
        "recommendations": hrf_experiment_output_path().joinpath("models/results/recommendations/"),
        "trained_models": hrf_experiment_output_path().joinpath("models/trained_models/")
    },
    "datasets": hrf_experiment_output_path().joinpath("datasets/"),
    "preprocessing": {
        "folds": {
            "train": hrf_experiment_output_path().joinpath("preprocessing/folds/train/"),
            "validation": hrf_experiment_output_path().joinpath("preprocessing/folds/validation/")
        }
    },
    "evaluate": {
        "metrics": hrf_experiment_output_path().joinpath("evaluate/metrics/"),
        "statistics": hrf_experiment_output_path().joinpath("evaluate/statistics/")
    },
    "visualization": {
        "static": hrf_experiment_output_path().joinpath("visualization/static/"),
        "interactive": hrf_experiment_output_path().joinpath("visualization/interactive/")
    }
}


def remove_files_from_many_directories(folders: dict):
    for value in folders.values():
        print("Removendo arquivos do diretório: ", value)
        remove_files(value)


def remove_files(folder: str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_folder_object(key: str):
    return folders.get(key, None)


def remove_all(folder_object):
    if folder_object is None:
        raise Exception("Não existe nenhuma pasta existente para o parâmetro passado")

    if isinstance(folder_object, dict):
        remove_files_from_many_directories(folder_object)
    else:
        remove_files(folder_object)


def clean_experiment_output(items_to_remove: str | list):
    key = None
    keys = []
    if isinstance(items_to_remove, str):
        key = items_to_remove
        folder_object = get_folder_object(key)
        remove_all(folder_object)
    elif isinstance(items_to_remove, list):
        keys = items_to_remove
        for key in keys:
            folder_object = get_folder_object(key)
            remove_all(folder_object)


clean_experiment_output(
    [
        "datasets",
        "evaluate",
        "models",
        "preprocessing",
        "visualization"
    ]
)


import pytest
from src.utils import *

def test_hrf_experiment_output_task():
    hrf_path = hrf_experiment_output_path()
    root_path = get_project_root()
    experiment_path = "experiment_output/"
    isEqual = hrf_path == root_path.joinpath(experiment_path)
    print("isEqual: ", isEqual)
    assert isEqual == True
    experiment_path = "experiment/"
    isEqual = hrf_path == root_path.joinpath(experiment_path)
    assert isEqual == False

def test_process_parameters():
    parameters = {
        'key1': "",
        "keyX": "",
        "keyy": ""
    }
    default_keys = {'key1', 'key2', 'key3'}


    with pytest.raises(Exception) as e:
        parameters = process_parameters(parameters, default_keys)
        assert e.type == KeyError


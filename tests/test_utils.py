import pytest
from src.utils import *
from src.data.movielens import MovieLens


movielens = MovieLens({
    'proportion': "ml-latest-small"
})
ratings = movielens.ratings

def test_create_directory():
    pass

def test_check_if_directory_exists():
    pass
def test_hrf_experiment_output_task():
    hrf_path = hrf_experiment_output_path()
    root_path = get_project_root()
    experiment_path = "experiment_output/"
    isEqual = hrf_path == root_path.joinpath(experiment_path)
    print("isEqual: ", isEqual)
    assert isEqual is True
    experiment_path = "experiment/"
    isEqual = hrf_path == root_path.joinpath(experiment_path)
    assert isEqual is False


def test_convert_json_attribute_values_to_python():
    parameters = {
        "key1": "None",
        "key2": "true",
        "key3": "false",
        "key4": 44.0
    }
    to_python_attrs = convert_json_attribute_values_to_python(parameters)
    print("to python attrs: ", to_python_attrs)

    isIncorrectValue = False
    for value in to_python_attrs.values():
        if value == "None" or value == "true" or value == "false":
            isIncorrectValue = True

    assert isIncorrectValue == False
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


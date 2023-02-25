from src.data.loader import Loader
from src.utils import hrf_external_path, hrf_experiment_output_path
import dict2xml

loader = Loader()

CF_QUALITATIVE_METRICS = {
    'gini': 'QualitativeMetrics.GiniIndex',
    'person_correlation': 'QualitativeMetrics.PearsonCorrelation',
    'pqmean': 'QualitativeMetrics.PqMean',
    'standard_deviation': 'QualitativeMetrics.StandardDeviation'
}

CF_QUANTITATIVE_METRICS = {
    'log_of_date_ratings': 'QuantitativeMetrics.LogOfDateRatings',
    'log_of_qtd_ratings': 'QuantitativeMetrics.LogOfQtdRatings',
    'log_sdev_date': 'QuantitativeMetrics.LogSdevDate',
    'normalized_proportion_of_common_ratings': 'QuantitativeMetrics.NormalizedProportionOfCommomRatings',
    'normalized_proportion_of_ratings': 'QuantitativeMetrics.NormalizedProportionOfRatings',
    'pr_date_ratings': 'QuantitativeMetrics.PRDateRatings',
    'proportion_of_common_ratings': 'QuantitativeMetrics.ProportionOfCommomRatings',
    'proportion_of_ratings': 'QuantitativeMetrics.ProportionOfRatings',
    'ratings_mean': 'QuantitativeMetrics.RatingsMean'
}


CB_METRICS = [
    'cosine',
    'dice',
    'jaccard',
    'entropy'
]


def read_json_file():
    config_obj = loader.load_json_file("config.json")
    experiments = config_obj['experiments']
    return experiments


def get_metafeatures_obj(experiments):
    return experiments.get('metafeatures')


def create_initial_xml_file_structure() -> dict:
    return {
        "calculator": {}
    }


def get_globals(experiment):
    parameters = experiment.get('parameters')
    global_key = parameters.get('global', None)

    if global_key is None:
        return global_key

    #Para garantir que haverá a chave exitirá
    global_obj = {
        "global": global_key
    }
    return global_obj


def get_instances(experiment):
    parameters = experiment.get("parameters")
    instances = parameters.get('instances', None)

    if instances is None:
        return instances

    if len(instances) == 0:
        return None

    return instances

def select_cf_metric(metric_type:str):
    metric_type = metric_type.lower()

    selected_metric = CF_QUALITATIVE_METRICS.get(metric_type, None)

    if selected_metric is not None:
        return selected_metric

    selected_metric = CF_QUANTITATIVE_METRICS.get(metric_type, None)

    if selected_metric is not None:
        return selected_metric

    return None



def transform_instances_to_xml(global_dict = None, instances = []):
    basePath = hrf_external_path().joinpath("metric_calculator/")
    cf_output_path = hrf_experiment_output_path().joinpath("metafeatures/collaborative/")
    cb_output_path = hrf_experiment_output_path().joinpath("metafeatures/contentbased/")

    obj = {}
    #Adicionando estrutura global ao objeto final
    obj.update(global_dict)


    for ins in instances:
        class_name = ins.get('class_name', None)
        class_name = class_name.lower()
        ins_params = ins.get('parameters', None)

        print("Name of metafeature: ", class_name)

        metric = None

        if ins_params.get('type') == 'collaborative':
            metric = select_cf_metric(class_name)
            print("Collaborative metric: ", metric)
        elif ins_params.get('type') == 'content-based':
            metric = CB_METRICS.index(class_name)
            print("Content based metric: ", metric)




        process_obj = {
            "process": {
                "type": ins_params.get('type'),
                "metric": metric,
                "basePath": str(basePath)
            }
        }

        obj.update(process_obj)

    return dict2xml.dict2xml(obj)



experiments = read_json_file()
experiment = experiments[0]
metafeatures = get_metafeatures_obj(experiment)
print(metafeatures)
global_info = get_globals(metafeatures)
print("globalInfo: \n", global_info)
instances = get_instances(metafeatures)

final_obj = transform_instances_to_xml(global_info, instances)
print("final obj: \n", final_obj)

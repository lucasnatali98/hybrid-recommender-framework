
from src.instance_factory import InstanceFactory

def create_experiment_instances(config_obj):

    instance_factory = InstanceFactory(config_obj)

    pre_processing_instance_dict = instance_factory.get_instance_from_config_obj("PreProcessingContainer")

    metrics_instance_dict = instance_factory.get_instance_from_config_obj("MetricsContainer")
    metafeatures_instance_dict = instance_factory.get_instance_from_config_obj("MetaFeatureContainer")
    recommenders_instance_dict = instance_factory.get_instance_from_config_obj("RecommendersContainer")
    visualization_instance_dict = instance_factory.get_instance_from_config_obj("VisualizationContainer")
    results_instance_dict = instance_factory.get_instance_from_config_obj("ResultsContainer")

    preprocessing_instance = instance_factory.create_instance(pre_processing_instance_dict)
    metrics_instance = instance_factory.create_instance(metrics_instance_dict)
    metafeatures_instance = instance_factory.create_instance(metafeatures_instance_dict)
    recommenders_instance = instance_factory.create_instance(recommenders_instance_dict)
    visualization_instance = instance_factory.create_instance(visualization_instance_dict)
    results_instance = instance_factory.create_instance(results_instance_dict)

    return {
        "preprocessing": preprocessing_instance,
        "metrics": metrics_instance,
        "metafeatures": metafeatures_instance,
        "visualization": visualization_instance,
        "recommenders": recommenders_instance,
        "results": results_instance
    }


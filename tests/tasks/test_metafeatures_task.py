from src.tasks.metafeatures_task import MetaFeaturesTask

metafeature_task = MetaFeaturesTask()


class TestMetaFeaturesTask:
    def test_create_command_to_metrics_calculator(self):
        command = metafeature_task.create_command_to_metrics_calculator()
        print("olha o comando ae: ", command)
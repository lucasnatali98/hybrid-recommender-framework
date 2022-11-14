import subprocess
class MetricCalculator:
    def __init__(self):
        pass

    def execute(self, database, fold, eval, stats, **kwargs):
        """
        Função para realizar a execução do cálculo das métricas

        @param database:
        @param fold:
        @param eval:
        @param stats:
        @param kwargs:
        @return:
        """
        output = subprocess.call(['java', '-jar', database, fold, eval, stats])
        return output
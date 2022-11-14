import subprocess
import sys, os


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


metric_calcutor = MetricCalculator()

database_arg = sys.argv[0]
fold_arg = sys.argv[1]
eval_arg = sys.argv[2]
stats_arg = sys.argv[3]
#Definir restante dos possíveis parâmetros


result = metric_calcutor.execute(
    database=database_arg,
    fold=fold_arg,
    eval=eval_arg,
    stats=stats_arg
)

print(result)
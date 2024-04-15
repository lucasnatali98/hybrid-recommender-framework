from src.metrics.metric import RankingMetric
import lenskit.metrics.topn as lenskit_topn
from sklearn.metrics import ndcg_score
from src.utils import process_parameters
import pandas as pd
import numpy as np


class NDCG(RankingMetric):
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        """
        Avalia a métrica de NDCG (Normalized Discounted Cumulative Gain).

        Parâmetros:
            predictions (pd.Series): Predições do modelo de recomendação.
            truth (pd.DataFrame): DataFrame contendo os ratings de cada item para o usuário.
            **kwargs: Parâmetros adicionais.

        Retorna:
            float: O valor do NDCG.
        """
        raise NotImplementedError



class LenskitNDCG(NDCG):
    def __init__(self, parameters: dict) -> None:
        """
        Inicializa a métrica NDCG utilizando a implementação do Lenskit.

        Parâmetros:
            parameters (dict): Parâmetros adicionais
        """
        super().__init__(parameters)
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)

    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        """
         Avalia a métrica de NDCG utilizando a implementação do Lenskit.

         Parâmetros:
             predictions (pd.Series): Predições do modelo de recomendação.
             truth (pd.DataFrame): DataFrame contendo os ratings de cada item para o usuário.
             **kwargs: Parâmetros adicionais

         Retorna:
             float: O valor do NDCG calculado pelo Lenskit.
         """
        return lenskit_topn.ndcg(predictions, truth)


class SklearnNDCG(NDCG):
    def evaluate(self, predictions: pd.Series, truth: pd.Series, **kwargs):
        """
        Avalia a métrica de NDCG utilizando a implementação do Scikit-learn.

        Parâmetros:
            Parâmetros:
            predictions (pd.Series): Predições do modelo de recomendação.
            Predictions exemplo:
                    user     item  score       algorithm_name
            0         1        3  0.944695          nsga2
            1         1        5  0.910737          nsga2
            2         1       12  0.970244          nsga2
            3         1       17  0.920765          nsga2
            4         1       23  0.973771          nsga2
            ...     ...      ...       ...            ...
            592807  610  5931596  0.912676          nsga2
            592808  610  5931606  0.957475          nsga2
            592809  610  5931610  0.918153          nsga2
            592810  610  5931620  0.995429          nsga2
            592811  610  5931621  0.929348          nsga2

            truth (pd.DataFrame): DataFrame contendo os ratings de cada item para o usuário.
            truth exemplo:
                   user  item  rating
            0      1002  1093    0.75
            1      1002  1094    1.00
            2      1002  1120    0.75
            3      1002  1183    0.50
            4      1002  1189    1.00
            ...     ...   ...     ...
            80116    99   527    0.75
            80117    99   588    1.00
            80118    99   709    0.25
            80119    99   919    1.00
            80120    99   920    0.50

        Retorna:
            float: O valor do NDCG calculado pelo Scikit-learn.
        """
        merged_df = pd.merge(predictions, truth, on=['user', 'item'], how='inner')
        user_id = predictions['user'].iloc[0]
        user_ratings = merged_df[merged_df['user'] == user_id]
        predictions_array = predictions['score'].values.reshape(1, -1)
        truth_array = user_ratings['rating'].values.reshape(1, -1)
        return ndcg_score(y_true=truth_array, y_score=predictions_array)

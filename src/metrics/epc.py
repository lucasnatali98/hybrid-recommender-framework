from src.metrics.metric import NoveltyMetric
import pandas as pd

class NOVELTY(NoveltyMetric):
    """
    Classe abstrata representando uma métrica de novidade.
    """

    def evaluate(self, predictions: pd.Series, features: pd.Series, **kwargs):
        """
        Método abstrato para calcular a métrica de novidade.
        """
        raise NotImplementedError

    def get_relevance_item(self, item, ratings, threshold=None):
        """
        Determina a relevância de um item com base em sua classificação em comparação com um limiar ou classificação média.

        Parâmetros:
            item (int): O ID do item para verificar a relevância.
            ratings (DataFrame): DataFrame contendo classificações de usuário-item.
            threshold (float ou None): Limiar de relevância. Se None, a classificação média é usada.

        Retorna:
            int: 1 se a classificação do item for maior que o limiar ou a classificação média (se o limiar for None), caso contrário, 0.
        """
        item_ratings = ratings[ratings['item'] == item]

        if len(item_ratings) == 0:
            return 0

        item_rating = item_ratings.iloc[0]['rating']

        avg_rating = item_ratings['rating'].mean()

        if threshold is not None:
            if item_rating >= threshold:
                return 1
            else:
                return 0
        else:
            return 1 if item_rating > avg_rating else 0

    def no_relevance(self):
        """
        Retorna o valor de relevância para itens não relevantes.
        """
        return 1;

    def reciprocal_discount(self, position_recommendation):
        """
        Retorna o desconto recíproco para uma posição de recomendação dada.

        Parâmetros:
            position_recommendation (int): A posição da recomendação.

        Retorna:
            float: O desconto recíproco para a posição de recomendação.
        """
        return 1 / (position_recommendation + 1.0)

def generate_item_frequency_dict(ratings_df):
    """
    Gera um dicionário de frequência de itens com base em um DataFrame de classificações de usuário-item.

    Parâmetros:
        ratings_df (DataFrame): DataFrame contendo classificações de usuário-item.

    Retorna:
        dict: Um dicionário de frequência de itens.
        int: O número total de usuários.
    """
    item_frequency_dict = {}
    unique_users = set()

    for index, row in ratings_df.iterrows():
        item = int(row['item'])
        user = row['user']
        item_frequency_dict[item] = item_frequency_dict.get(item, 0) + 1
        unique_users.add(user)

    num_users = len(unique_users)
    return item_frequency_dict, num_users

class EPC(NOVELTY):
    """
    Classe para calcular a métrica de Expected Popularity Complement (EPC).
    """

    def __init__(self, cutoff, preferences_dict=None, num_users_with_preference=None, threshold=None):
        """
        Inicializa a classe EPC.

        Parâmetros:
            cutoff (int): O número de recomendações consideradas.
            preferences_dict (dict): Dicionário de frequência de itens.
            num_users_with_preference (int): O número total de usuários com preferências registradas.
            threshold (float): O limiar de relevância.
        """
        self.cutoff = cutoff
        self.item_frequency_dict = preferences_dict
        self.num_users = num_users_with_preference
        self.threshold = threshold

    def calculate_epc(self, rec_list, user_ratings):
        """
        Calcula a pontuação EPC para uma lista de recomendações.

        Parâmetros:
            rec_list (list): Lista de itens recomendados.
            user_ratings (DataFrame): DataFrame contendo classificações de usuário-item.

        Retorna:
            float: A pontuação EPC calculada.
        """
        if self.item_frequency_dict is None or self.num_users is None:
            self.item_frequency_dict, self.num_users = generate_item_frequency_dict(user_ratings)

        item_novelty_dict = {item: 1 - (frequency / self.num_users) for item, frequency in self.item_frequency_dict.items()}

        epc_score = 0
        norm = 0

        for index_item, item in enumerate(rec_list[:self.cutoff]):
            relevance = self.get_relevance_item(item, user_ratings, self.threshold)
            discount = self.reciprocal_discount(index_item)

            epc_score += discount * relevance * item_novelty_dict.get(item, 1)
            norm += discount

        if norm > 0:
            epc_score /= norm
        return epc_score

    def evaluate(self, predictions: pd.DataFrame, truth: pd.DataFrame, **kwargs):
        """
        Calcula a pontuação EPC para um conjunto de predições.

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
            float: A pontuação EPC calculada.
        """
        rec_list = predictions['item'].tolist()
        epc_score = self.calculate_epc(rec_list, truth)
        return epc_score

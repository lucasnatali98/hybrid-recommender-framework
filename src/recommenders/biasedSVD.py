from src.recommenders.recommender import Recommender


class BiasedSVD(Recommender):
    def __init__(self, parameters: dict) -> None:
        """

        """

        self.process_parameters(parameters)

        self.features = parameters['features']
        self.damping = parameters['damping']
        self.bias = parameters['bias']
        self.algorithm = parameters['algorithm']

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """


        default_keys = [
            'damping',
            'features',
            'bias',
            'algorithm'
        ]
        parameters_keys = parameters.keys()

        for key in default_keys:
            if key not in parameters_keys:
                raise KeyError("A chave obrigatória {} não foi informada no arquivo de configuração".format(key))

        return parameters

    def predict_for_users(self, users, items, ratings):
        """

        @param users:
        @param items:
        @param ratings:
        @return:
        """
        pass

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        pass

    def recommend(self, user, n, candidates, ratings):
        """

        @param user:
        @param n:
        @param candidates:
        @param ratings:
        @return:
        """
        pass

    def get_params(self, deep=True):
        """

        @param deep:
        @return:
        """
        pass

    def fit(self, rating, **kwargs):
        """

        @param rating:
        @param kwargs:
        @return:
        """
        pass
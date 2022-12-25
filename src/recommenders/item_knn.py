from src.recommenders.recommender import Recommender
from lenskit.algorithms import item_knn

class ItemKNN(Recommender):
    def __init__(self, parameters: dict) -> None:
        """
        
        """

        self.process_parameters(parameters)
        self.max_number_neighbors = parameters['maxNumberNeighbors']
        self.min_number_neighbors = parameters['minNumberNeighbors']
        self.save_nbrs = parameters['saveNeighbors']
        self.feedback = parameters['feedback']
        self.aggregate = parameters['aggregate']
        self.use_ratings = parameters['use_ratings']

        self.ItemKNN = item_knn.ItemItem(
            nnbrs=self.max_number_neighbors,
            min_nbrs=self.min_number_neighbors,
            save_nbrs=self.save_nbrs,
            feedback=self.feedback,
            aggregate=self.aggregate,
            use_ratings=self.use_ratings
        )

    def process_parameters(self, parameters: dict) -> dict:
        """

        @param parameters: objeto com os parâmetros da classe
        @return: dicionário atualizado com esses mesmos parâmetros
        """


        default_keys = [
            'maxNumberNeighbors',
            'minNumberNeighbors',
            'saveNeighbors',
            'feedback'
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
        return self.ItemKNN.predict_for_user(users, items, ratings)

    def predict(self, pairs, ratings):
        """

        @param pairs:
        @param ratings:
        @return:
        """
        return self.ItemKNN.predict(pairs, ratings)

    def recommend(self, user, n, candidates, ratings):
        """

        @param user:
        @param n:;
        @param candidates:
        @param ratings:
        @return:
        """
        pass

    def get_params(self, deep = True):
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
        self.ItemKNN.fit(rating)

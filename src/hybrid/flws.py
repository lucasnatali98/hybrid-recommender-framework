from src.hybrid.hybrid import HybridWeighted
from src.utils import process_parameters
from pandas import DataFrame, Series, read_csv

from src.metafeatures.metafeature import read_metafeatures_textfiles
from src.data.movielens import MovieLens
from src.data.loader import Loader


class FLWS(HybridWeighted):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        super().__init__(parameters)
        default_keys = set()

        parameters = process_parameters(parameters, default_keys)


    def combine_metafeature_with_predictions(self, metafeature: DataFrame, predictions: DataFrame) -> DataFrame:
        print(metafeature)
        print(predictions)

        return predictions

    def set_weights(self, weights):
        pass
    def predict(self, metafeatures, predictions):
        pass
    def run(self, metafeatures: DataFrame, predictions: DataFrame) -> DataFrame:
        """

        @return:
        """
        pass


flws = FLWS({
    "shit": True
})
predict_result = read_csv("batch_predict_result.csv", index_col=[0])

print(predict_result)

metafeatures = read_metafeatures_textfiles()
cf_metafeatures = metafeatures.get('collaborative')
cb_metafeatures = metafeatures.get('content-based')



gini_item = None
gini_item_user = None
gini_user = None

print("---------------------------------------------------------------")

for cfm in cf_metafeatures:
    for key,value in cfm.items():
        if key == "Gini_Item":
            gini_item = value
        if key == "Gini_ItemUser":
            gini_item_user = value
        if key == "Gini_User":
            gini_user = value

print("gini item: ", gini_item)
print("gini item user: ", gini_item_user)
print("gini user: ", gini_user)


flws
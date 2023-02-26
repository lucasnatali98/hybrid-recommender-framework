from src.hybrid.hybrid import HybridWeighted
from src.utils import process_parameters
from pandas import DataFrame, Series

from src.metafeatures.metafeature import read_metafeatures_textfiles
from src.data.movielens import MovieLens
from src.data.loader import Loader


class FLWS(HybridWeighted):
    def __init__(self, parameters: dict) -> None:
        """
        
        """
        super().__init__()
        default_keys = set()
        parameters = process_parameters(parameters, default_keys)


    def run(self, metafeatures: DataFrame, predictions: DataFrame) -> DataFrame:
        """

        @return:
        """
        pass



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


from RelevanceModels.UserThresholdNDCGRelevanceModel import *
from RelevanceModels.UserThresholdBinaryRelevanceModel import *

from NoveltyModels.UserPCItemNoveltyModel import *
from NoveltyModels.UserPDItemNoveltyModel import *

from DiscountModels.NoDiscountModel import *

from DistanceModels.CosineFeatureItemDistanceModel import *

from NDCG import *
from Precision import *
from Recall import *
from F1 import *
from EPC import *
from EPD import *
from EILD import *

import sys
sys.path.append('../read')

import readRecommendation
import readThresholds
import readFeatures

if __name__ == "__main__":
	ratings = readRecommendation.read("../BD/Sample2345.txt")
	thresholds = readThresholds.read("../BD/usersThreshold.txt")
	recommendation = readRecommendation.read("../BD/Sample2345.txt")
	feature_maps = readFeatures.read("../BD/u.item.attributes") 
	#feature_maps[0] = map[item] => [(feature, value)], feature_maps[0] = map[feature] => [(item, value)]

	#relevanceModel = UserThresholdNDCGRelevanceModel(ratings, None, thresholds, 0.5)
	relevanceModel = UserThresholdBinaryRelevanceModel(ratings, None, thresholds, 0.5)

	discountModel = NoDiscountModel()

	distanceModel = CosineFeatureItemDistanceModel(feature_maps[0], feature_maps[1])

	#noveltyModel = UserPCItemNovelty(recommendationData) # arquivo com todas as recomendacoes de itens
	noveltyModel = UserPDItemNovelty(ratings, distanceModel)

	#metric = NDCG(20, relevanceModel)
	#metric = Precision(20, relevanceModel)
	#metric = Recall(20, relevanceModel)
	#metric = F1(20, relevanceModel, False, None)
	#metric = EPC(20, relevanceModel, noveltyModel, discountModel)
	#metric = EILD(20, relevanceModel, discountModel, distanceModel)
	metric = EPD(20, relevanceModel, noveltyModel, discountModel)

	count = 0
	for uid in ratings.keys():
		if (count == 100): break
		#print (uid)
		print (metric.evaluate(recommendation[uid], uid))
	
	

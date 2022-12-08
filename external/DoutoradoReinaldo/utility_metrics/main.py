import read.readRecommendationLazy
import read.readRecommendation
import read.readFeatures

from metrics.NoveltyModels.UserPCItemNoveltyModel import *
from metrics.NoveltyModels.UserPDItemNoveltyModel import *

from metrics.DistanceModels.CosineFeatureItemDistanceModel import *

from UtilityModels.UtilityMetrics.AccuracyUtilityMetric import *
from UtilityModels.UtilityMetrics.NoveltyUtilityMetric import *
from UtilityModels.UtilityMetrics.DiversityUtilityMetric import *

from UtilityModels.UtilityModels import *



def R(utility_lists): # utility_lists = ([Ra], [Rmaxa])
	denominador = sum([Rmaxa for Rmaxa in utility_lists[1] ])
	return sum([Ra/denominador for Ra in utility_lists[0]])	

if __name__ == "__main__":

	#TODO criar uma classe para substituir o main para chamadas externas.

	feature_maps = read.readFeatures.read("BD/u.item.attributes") 

	distanceModel = CosineFeatureItemDistanceModel(feature_maps[0], feature_maps[1])

	Ra = []
	Rmaxa = []

	ratings = read.readRecommendation.read("BD/Sample2.txt") # esse e o arquivo usado como base para os utilityModels

	#noveltyModel = UserPCItemNovelty(ratings)
	noveltyModel = UserPDItemNovelty(ratings, distanceModel)

	count = 0
	for t in read.readRecommendationLazy.read("BD/Sample2345.txt"): # aqui deveria vir o arquivo ordenado com recomendacoes a cada usuario
		if (count == 10): break

		#print(t)
		uid = t[0]
		usr_rank = t[1] #lista rankeada do usuario
			
		noveltyModel.evaluationStart(uid)

		#utilityMetric = DiversityUtilityMetric(distanceModel, usr_rank) 
		#utilityMetric = NoveltyUtilityMetric(noveltyModel) 
		#utilityMetric = AccuracyUtilityMetric(0.5) # param = neutral_vote

		utilityModel = BreeseUtilityModel(utilityMetric, usr_rank, 5)  #o segundo parametro e a lista rankeada de recomendacoes a ser avaliada, seguido pelo halflife
		utilityModel.calcUtility()
		Ra.append(utilityModel.getUtility())
		Rmaxa.append(utilityModel.getMaxUtility())

		count += 1
	utility_lists = (Ra, Rmaxa)
	print R(utility_lists)

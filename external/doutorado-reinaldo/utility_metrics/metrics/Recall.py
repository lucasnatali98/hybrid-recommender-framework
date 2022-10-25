from UtilityModels.UtilityMetrics.BaseUtilityMetric import *

class Recall(BaseUtilityMetric):
	def __init__(self, cutoff, relModel):
		self.cutoff = cutoff
		self.relModel = relModel

	def evaluate(self, recommendation):
		relevantsTotal = len(self.relModel.getRelevantItems())
		if relevantsTotal == 0: return 0.0
		return len([iv for iv in recommendation if self.relModel.isRelevant(iv[0])]) / float(relevantsTotal)
		
		
				


from UtilityModels.UtilityMetrics.BaseUtilityMetric import *

class Precision(BaseUtilityMetric):
	def __init__(self, cutoff, relModel):
		self.cutoff = cutoff
		self.relModel = relModel

	def evaluate(self, recommendation):
		return len([iv for iv in recommendation if self.relModel.isRelevant(iv[0])]) / float(self.cutoff)
				


from .Precision import *
from .Recall import *
from .AllUserItemAverageRecommendationMetric import *
from UtilityModels.UtilityMetrics.BaseUtilityMetric import *


class F1(BaseUtilityMetric):
	def __init__(self, cutoff, relModel, ignoreNaN, objectiveWeightsProcessor):
		precision = Precision(cutoff, relModel)
		self.precision = AllUserItemAverageRecommendationMetric(precision, ignoreNaN, objectiveWeightsProcessor)
		recall = Recall(cutoff, relModel)
		self.recall = AllUserItemAverageRecommendationMetric(recall, ignoreNaN, objectiveWeightsProcessor)

	def evaluate(self, recommendation):
		precision_v = self.precision.evaluate(recommendation)
		recall_v = self.recall.evaluate(recommendation)
		if (precision_v == 0 and recall_v == 0): return 0.0
		return 2*(precision_v*recall_v)/(precision_v+recall_v)


from .BaseUtilityMetric import *

class AccuracyUtilityMetric(BaseUtilityMetric):
	def __init__(self, neutral_vote):
		self.d = neutral_vote

	def evaluate(self, iv): #iv = (item_id, value)
		return max(iv[1]-self.d, 0.0)

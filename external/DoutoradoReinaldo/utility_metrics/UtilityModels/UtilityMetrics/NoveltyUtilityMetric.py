from .BaseUtilityMetric import *

class NoveltyUtilityMetric(BaseUtilityMetric):
	def __init__(self, noveltyModel): # user_ratings = [(item_id, value)]
		self.noveltyModel = noveltyModel

	def evaluate(self, iv): #iv = (item_id, value)
		return self.noveltyModel.novelty(iv[0])

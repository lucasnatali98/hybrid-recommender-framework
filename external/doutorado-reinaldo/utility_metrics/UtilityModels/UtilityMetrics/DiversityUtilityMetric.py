from .BaseUtilityMetric import *

class DiversityUtilityMetric(BaseUtilityMetric):
	def __init__(self, distanceModel, user_ratings): # user_ratings = [(item_id, value)]
		self.ratings = user_ratings
		self.distanceModel = distanceModel

	def evaluate(self, ivA): #iv = (item_id, value)
		s = 0.0
		total = len(self.ratings)
		for ivB in self.ratings:
			if ivA[0] == ivB[0]:
				total -= 1
				continue
			s+= self.distanceModel.distance(ivA[0], ivB[0]) / total
		return s	

import math

class AllUserItemAverageRecommendationMetric:
	def __init__(self, metric, ignoreNaN, objectiveWeightsProcessor):
		self.metric = metric
		self.sum = 0
		self.numUsers = 0
		self.allUsers = False
		self.ignoreNaN = ignoreNaN
		self.objectiveWeightsProcessor = objectiveWeightsProcessor
		self.usersValues = dict()

	def addAndEvaluate(self, recommendation, user_id):
		v = self.metric.evaluate(recommendation, user_id)
		if self.objectiveWeightsProcessor is not None:
			self.objectiveWeigthsProcessor.put(user_id, v)
		if not self.ignoreNaN and not math.isnan(v):
			self.sum = self.sum + v
		if not self.allUsers:
			self.numUsers+=1
		return v

	def add(self, recommendation, user_id):
		self.addAndEvaluate(recommendation, user_id)

	def evaluate(self):
		return self.sum/self.numUsers

	

        
	
		
		

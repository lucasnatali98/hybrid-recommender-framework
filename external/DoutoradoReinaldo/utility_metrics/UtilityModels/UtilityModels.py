
class BaseUtilityModel():
	def __init__(self, metric):
		self.metric = metric

	def calcUtility(self):
		raise NotImplementedError


class BreeseUtilityModel(BaseUtilityModel):
	def __init__(self, utility_metric, ranked_list, halflife, incJ):  # ranked_list =[(item, value)], d=neutral_vote, a=halflife
		#super(BaseUtilityModel, self).__init__(utility_metric) #TODO: Arrumar
		self.metric = utility_metric
		self.ranked_list = ranked_list
		self.a = halflife
		self.incJ = incJ # boolean indicando para sempre incrementar J

	def calcUtility(self):  # self.ranked_list=[(item, value)], d=neutral_vote, a=halflife
		su  = 0.0  # utility sum
		smu = 0.0  # max_utility sum
		j = 0
		currentScore = None
		for iv in self.ranked_list:
			utility = self.metric.evaluate(iv)
			smu += utility
			su += utility / pow(2.0, (float(j) / (self.a - 1)))
			if self.incJ or iv[1] != currentScore:
				j += 1
				currentScore = iv[1]
		self.utility = su
		self.max_utility = smu

	def getUtility(self):
		return self.utility

	def getMaxUtility(self):
		return self.max_utility

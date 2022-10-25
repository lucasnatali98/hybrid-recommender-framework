

class UserThresholdBinaryRelevanceModel:
	def __init__(self, testData, testFilter, thresholdMap, defaultThreshold):
		self.testData = testData
		self.testFilter = testFilter
		self.thresholdMap = thresholdMap
		self.defaultThreshold = defaultThreshold

	def evaluationStart(self, user):
		self.user = user
		self.relevantItems = set()
		for iv in filter(self.filtro, self.testData[user]):
			if (self.defaultThreshold if self.thresholdMap is None else self.thresholdMap[user]) <= iv[1]:
				self.relevantItems.add(iv[0])
		
	def isRelevant(self, i):
		return i in self.relevantItems

	def getRelevantItems(self):
		return self.relevantItems

	def filtro(self, iv):
		return (self.testFilter is None or iv[0] in self.testFilter[self.user]) and iv[1] >= ( self.thresholdMap[self.user] if self.user in self.thresholdMap else self.defaultThreshold)	

	def gain(self, item_id):
		return 1.0 if self.isRelevant(item_id) else 0.0

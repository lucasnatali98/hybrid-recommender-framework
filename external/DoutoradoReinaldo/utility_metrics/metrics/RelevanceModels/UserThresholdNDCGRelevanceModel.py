import math

class UserThresholdNDCGRelevanceModel:
	def __init__(self, testData, testFilter, thresholdMap, defaultThreshold):
		self.testData = testData
		self.testFilter = testFilter
		self.thresholdMap = thresholdMap
		self.defaultThreshold = defaultThreshold

	def evaluationStart(self, user):
		self.user = user
		self.gainMap = dict()
		for iv in filter(self.filtro, self.testData[user]):
			self.setGain(iv) 

	def filtro(self, iv):
		return (self.testFilter is None or iv[0] in self.testFilter[self.user]) and iv[1] >= ( self.thresholdMap[self.user] if self.user in self.thresholdMap else self.defaultThreshold)
		
	def setGain(self, iv):
		self.gainMap[iv[0]] = math.pow(2, iv[1] - (self.thresholdMap[self.user] if self.user in self.thresholdMap else self.defaultThreshold) + 1.0) - 1.0	
	
	def gain(self, id):
		if id in self.gainMap:
			return self.gainMap[id]
		else:
			return 0.0

	def getGainValues(self):
		return self.gainMap.values()
		
	
		
	

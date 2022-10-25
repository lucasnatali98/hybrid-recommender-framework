import math, threading

class CosineFeatureItemDistanceModelLock:
	def __init__(self, itemMap, featureMap):
		self.itemFeatureMap = itemMap
		self.featureItemMap = featureMap
		self.computedPairs = {}
		self.lock = threading.Lock()
	
	def distance(self, idIa, idIb):
		key = f'{min(idIa, idIb)}_{max(idIa, idIb)}'
		if key in self.computedPairs: return self.computedPairs[key]
		numerador = len([f for f in self.itemFeatureMap[idIa] if f in self.itemFeatureMap[idIb]])
		dA = len(self.itemFeatureMap[idIa])
		dB = len(self.itemFeatureMap[idIb])
		denominador = math.sqrt(dA*dB)
		valor = 1.0 - numerador/denominador
		with self.lock:
			self.computedPairs[key] = valor
		return valor


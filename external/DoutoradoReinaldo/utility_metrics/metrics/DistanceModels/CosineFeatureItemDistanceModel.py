import math


class CosineFeatureItemDistanceModel:
    def __init__(self, itemMap, featureMap):
        self.itemFeatureMap = itemMap
        self.featureItemMap = featureMap

    def distance(self, idIa, idIb):
        if idIa not in self.itemFeatureMap or idIb not in self.itemFeatureMap:
            return 0.0  # TODO: Retornar tamanho do vetor que existe?
        numerador = len([f for f in self.itemFeatureMap[idIa] if f in self.itemFeatureMap[idIb]])
        dA = len(self.itemFeatureMap[idIa])
        dB = len(self.itemFeatureMap[idIb])
        denominador = math.sqrt(dA * dB)
        return 1.0 - float(numerador) / denominador



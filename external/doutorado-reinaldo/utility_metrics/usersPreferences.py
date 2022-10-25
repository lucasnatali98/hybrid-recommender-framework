'''
PreProcessing.

Created on 07/02/2018
Updated on
@author: reifortes

Execution line: python3.4 ...
'''
import sys
import read.readFeatures
import read.readRecommendation
import read.readRecommendationLazy
from metrics.DistanceModels.CosineFeatureItemDistanceModel import *
from metrics.NoveltyModels.UserPCItemNoveltyModel import *
from UtilityModels.UtilityModels import *
from UtilityModels.UtilityMetrics.AccuracyUtilityMetric import *
from UtilityModels.UtilityMetrics.DiversityUtilityMetric import *
from UtilityModels.UtilityMetrics.NoveltyUtilityMetric import *


def calcUtility(utilityMetric, usr_rank):
    utilityModel = BreeseUtilityModel(utilityMetric, usr_rank, 5, False)
    utilityModel.calcUtility()
    if utilityModel.getMaxUtility() == 0: return float('nan')
    return utilityModel.getUtility() / utilityModel.getMaxUtility()


def readTestUsers(fileName):
    users = set()
    file = open(fileName, 'r')
    for line in file:
        line = line.strip().split()
        uid = int(line[0])
        users.add(uid)
    return users


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    homeDir         = sys.argv[1]
    featureMapsFile = sys.argv[2]
    trainFile       = sys.argv[3]
    testFile        = sys.argv[4]
    outFile         = open('%s/BD/%s' % (homeDir, sys.argv[5]), 'w')
    thresholdValue  = float(sys.argv[6] if len(sys.argv) > 6 else 0)
    print('- reading features.')
    featureMaps = read.readFeatures.read("%s/BD/%s" % (homeDir, featureMapsFile))
    print('- reading ratings.')
    ratings = read.readRecommendation.read("%s/BD/%s" % (homeDir, trainFile))
    print('- creating distance model.')
    distanceModel = CosineFeatureItemDistanceModel(featureMaps[0], featureMaps[1])
    print('- creating novelty model.')
    noveltyModel = UserPCItemNovelty(ratings)
    print('- processing bias.')
    testUsers = readTestUsers("%s/BD/%s" % (homeDir, testFile))
    for (uid, usr_rank) in read.readRecommendationLazy.read("%s/BD/%s" % (homeDir, trainFile)):
        if uid == None: break
        if uid not in testUsers: continue
        noveltyModel.evaluationStart(uid)
        utilityMetric = AccuracyUtilityMetric(thresholdValue)
        accuracyBias = calcUtility(utilityMetric, usr_rank)
        utilityMetric = DiversityUtilityMetric(distanceModel, usr_rank)
        dyversityBias = calcUtility(utilityMetric, usr_rank)
        utilityMetric = NoveltyUtilityMetric(noveltyModel)
        noveltyBias = calcUtility(utilityMetric, usr_rank)
        outFile.write('%s\t%.6f\t%.6f\t%.6f\n' % (uid, accuracyBias, dyversityBias, noveltyBias))
    outFile.close()
    print("Fim")

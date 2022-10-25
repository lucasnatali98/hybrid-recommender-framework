'''
Realiza avaliacao da utilidade de CB na recomendacao hibrida

ABORTADO: Pacote foi criado para a obtenção dos pesos de cada objetivo,
não é totalmente equivalente ao cálculo das métricas de avaliação.
As classes ciradas para as métricas, como F!, Precision e Recall precisam
ser revisadas.

Created on 27/11/2018
Updated on
@author: reifortes

Execution line: python3.7 ...
'''
import sys, glob, os
import read.readFeatures
import read.readThresholds
import read.readRecommendation
import read.readRecommendationLazy
from metrics.DistanceModels.CosineFeatureItemDistanceModel import *
from metrics.NoveltyModels.UserPCItemNoveltyModel import *
from UtilityModels.UtilityModels import *
from metrics.RelevanceModels.UserThresholdBinaryRelevanceModel import *
from metrics.F1 import *
from UtilityModels.UtilityMetrics.DiversityUtilityMetric import *
from UtilityModels.UtilityMetrics.NoveltyUtilityMetric import *



def calcUtility(utilityMetric, usr_rank):
    utilityModel = BreeseUtilityModel(utilityMetric, usr_rank, 5, False)
    utilityModel.calcUtility()
    if utilityModel.getMaxUtility() == 0: return float('nan')
    return utilityModel.getUtility() / utilityModel.getMaxUtility()



if __name__ == '__main__':
    print("Inicio")
    homeDir         = sys.argv[1]
    featureMapsFile = sys.argv[2]
    thresholdsFile  = sys.argv[3]
    trainFile       = sys.argv[4]
    testFile        = sys.argv[5]
    rankingFold     = '%s/%s' % (homeDir, sys.argv[6])
    outFold         = '%s/%s' % (homeDir, sys.argv[7])
    if not os.path.exists(outFold):
        os.makedirs(outFold)

    cutoff = 5 # avaliar apenas os 5 primeiros
    defaultThreshold = 0.6

    print('- reading features.')
    featureMaps = read.readFeatures.read("%s/BD/%s" % (homeDir, featureMapsFile))
    print('- reading thresholds.')
    if thresholdsFile == 'none': thresholds = None
    else: thresholds = read.readThresholds.read("%s/BD/%s" % (homeDir, thresholdsFile))
    print('- reading trainData.')
    trainData = read.readRecommendation.read("%s/BD/%s" % (homeDir, trainFile))
    print('- reading testData.')
    testData = read.readRecommendation.read("%s/BD/%s" % (homeDir, testFile))
    print('- creating distance model.')
    distanceModel = CosineFeatureItemDistanceModel(featureMaps[0], featureMaps[1])
    print('- creating novelty model.')
    noveltyModel = UserPCItemNovelty(trainData)

    print('- processing rankings.')
    relModel = UserThresholdBinaryRelevanceModel(testData, None, thresholds, defaultThreshold)
    rankingFiles = glob.glob('%s/%s' % (rankingFold, "*.txt"))
    for rankingFile in rankingFiles:
        alg = os.path.basename(rankingFile)
        outFile = open('%s/%s' % (outFold, alg), 'w')
        for (uid, usr_rank) in read.readRecommendationLazy.read(rankingFile, cutoff):
            if uid == None: break
            noveltyModel.evaluationStart(uid)

            utilityMetric = F1(cutoff, relModel, False, None)
            accuracyMeasure = calcUtility(utilityMetric, usr_rank)

            utilityMetric = DiversityUtilityMetric(distanceModel, usr_rank)
            diversityMeasure = calcUtility(utilityMetric, usr_rank)

            utilityMetric = NoveltyUtilityMetric(noveltyModel)
            noveltyMeasure = calcUtility(utilityMetric, usr_rank)

            outFile.write('%s\t%.6f\t%.6f\t%.6f\n' % (uid, accuracyMeasure, diversityMeasure, noveltyMeasure))

        outFile.close()
    print("Fim")

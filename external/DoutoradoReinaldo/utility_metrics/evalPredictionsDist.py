'''
Calcula a distância dos pesos do usuário para os pesos obtidos na recomendação
@author: reifortes
'''
import sys, os, csv, glob, math, traceback
import read.readFeatures
import read.readThresholds
import read.readRecommendation
import read.readRecommendationLazy
from metrics.DistanceModels.CosineFeatureItemDistanceModelLock import *
from metrics.NoveltyModels.UserPCItemNoveltyModel import *
from UtilityModels.UtilityModels import *
from UtilityModels.UtilityMetrics.AccuracyUtilityMetric import *
from UtilityModels.UtilityMetrics.DiversityUtilityMetric import *
from UtilityModels.UtilityMetrics.NoveltyUtilityMetric import *
from scipy.spatial import distance
import concurrent.futures


def readPreferences(fileName):
    users = {}
    tsv_reader = csv.reader(open(fileName, 'rt'), delimiter='\t')
    for aux, data in enumerate(tsv_reader):
        if 'nan' in data: continue
        values = [ float(x) for x in data[1:] ]
        s = sum(values)
        users[int(data[0])] = [ x/s for x in values ]
    return users


def calcUtility(utilityMetric, usr_rank):
    utilityModel = BreeseUtilityModel(utilityMetric, usr_rank, 5, False)
    utilityModel.calcUtility()
    if utilityModel.getMaxUtility() == 0: return float('nan')
    return utilityModel.getUtility() / utilityModel.getMaxUtility()


def computeDistance(p1, p2):
    return abs(distance.euclidean(p1, p2))


def processUser(userId, usr_rank, outfile):
    global thresholdValue, distanceModel, noveltyModel, usersWeights
    if userId not in usersWeights: return
    minScore = min([x[1] for x in usr_rank])
    if minScore < 0:
        minScore = abs(minScore)
        newRank = []
        for score in usr_rank: newRank.append( (score[0], score[1] + minScore) )
        usr_rank = newRank
    noveltyModel.evaluationStart(userId)
    utilityMetric = AccuracyUtilityMetric(thresholdValue)
    accuracyBias = calcUtility(utilityMetric, usr_rank)
    utilityMetric = DiversityUtilityMetric(distanceModel, usr_rank)
    diversityBias = calcUtility(utilityMetric, usr_rank)
    utilityMetric = NoveltyUtilityMetric(noveltyModel)
    noveltyBias = calcUtility(utilityMetric, usr_rank)
    # Levar isso para a análise de resultado
    # Acurácia não será nan, novidade e diversidade pode
    # Caso as duas sejam nan, ignore
    if math.isnan(diversityBias) and math.isnan(noveltyBias):
        print(f'{userId}: {accuracyBias} | {diversityBias} | {noveltyBias} | {usr_rank}')
        return
    # Caso novidade ou diversidade seja nan, assume o mesmo valor da outra
    if math.isnan(diversityBias): diversityBias = noveltyBias
    if math.isnan(noveltyBias): noveltyBias = diversityBias
    sumBias = accuracyBias + diversityBias + noveltyBias
    if sumBias == 0 or math.isnan(sumBias): return
    algWeights = [ accuracyBias / sumBias, diversityBias / sumBias, noveltyBias / sumBias ]
    try:
        dist = computeDistance(usersWeights[userId], algWeights)
    except Exception as e:
        print(f'Error computeDistance {outfile}: User {userId} | {usr_rank}')
        #traceback.print_exc()
    outfile.write(f'{userId}\t{dist}\n')


def processR(r):
    global resultsFolder, outFoldName, usersWeights, scikitFolder
    files = glob.glob(f'{resultsFolder.replace("xRx", r)}/*.txt')
    for file in files:
        try:
            baseName = os.path.basename(file)
            print(f'- Begin: {file}')
            inFile = open(file, 'r')
            outFold = f'{outFoldName.replace("xRx", r)}/'
            if not os.path.exists(outFold): os.makedirs(outFold)
            outfile = open(f'{outFold}{baseName}', 'w')
            outfile.write('id\tDist\n')
            line = inFile.readline()
            line = line.strip().split('\t')
            userId = int(line[0])
            itemId = int(line[1])
            score = float(line[2])
            id = userId
            usr_rank = [ (itemId, score) ]
            for line in inFile:
                line = line.strip().split('\t')
                userId = int(line[0])
                itemId = int(line[1])
                score = float(line[2])
                if id == userId:
                    usr_rank.append( (itemId, score) )
                else:
                    processUser(id, usr_rank, outfile)
                    id = userId
                    usr_rank = [ (itemId, score) ]
            processUser(id, usr_rank, outfile)
            outfile.close()
        except Exception as e:
            outfile.close()
            print(f'Error processing {file}: User {userId} | {usr_rank}')
            #traceback.print_exc()
        print(f'- End: {file}')


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    homeDir         = sys.argv[1] # Bookcrossing
    featureMapsFile = sys.argv[2] # u.item.attributes
    thresholdValue  = float(sys.argv[3]) # 0 -- não avaliaremos apenas itens relevantes para obter a importância de acurácia
    ratingsFile     = sys.argv[4] # Sample2345.txt
    userWeightsFile = sys.argv[5] # Sample2345-sortedByRating_BIAS_1.txt
    resultsFolder   = f'{homeDir}/{sys.argv[6]}' # ResultsFinal/Predictions/RxRx/F2345-1
    r1              = int(sys.argv[7])
    r2              = int(sys.argv[8])
    qtdThreads      = int(sys.argv[9])
    outFoldName     = f'{homeDir}/{sys.argv[10]}' # ResultsFinal/Dist/RxRx/F2345-1
    print('- reading features.')
    featureMaps = read.readFeatures.read("%s/BD/%s" % (homeDir, featureMapsFile))
    print('- reading ratings.')
    ratings = read.readRecommendation.read("%s/BD/%s" % (homeDir, ratingsFile))
    print('- creating distance model.')
    distanceModel = CosineFeatureItemDistanceModelLock(featureMaps[0], featureMaps[1])
    print('- creating novelty model.')
    noveltyModel = UserPCItemNovelty(ratings)
    print('- reading user\'s preferences.')
    usersWeights = readPreferences(f'{homeDir}/BD/{userWeightsFile}')
    print('- computing distances.')
    executor = concurrent.futures.ThreadPoolExecutor(qtdThreads)
    futures = [ executor.submit(processR, str(r)) for r in range(r1, r2+1) ]
    concurrent.futures.wait(futures)
    print("Fim")

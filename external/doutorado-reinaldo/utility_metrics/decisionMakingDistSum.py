'''
Escolhe uma solução com base nas soluções de uma busca MO.
@author: reifortes
'''
import sys, os, csv, glob
import read.readFeatures
import read.readRecommendation
import read.readRecommendationLazy
from metrics.DistanceModels.CosineFeatureItemDistanceModel import *
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
    return abs(utilityModel.getUtility() / utilityModel.getMaxUtility())


def readSklFeatures(scikitFolder, user, hybrid, fSel):
    sklFeatures = {}
    sklFile = open(f'{scikitFolder}/{hybrid}{"-sel" if fSel else "-all"}.train', 'r')
    keysFile = open(f'{scikitFolder}/keys.train', 'r')
    for features, keys in zip(sklFile, keysFile):
        keys = keys.strip().split(',')
        if int(keys[0]) != user: continue
        item = int(keys[1])
        features = features.strip().split()[1:]
        sklFeatures[item] = [ float(f.split(':')[1]) for f in features ]
    sklFile.close()
    keysFile.close()
    return sklFeatures


def computeScores(vars, sklFeatures):
    scores = {}
    min = float('inf')
    for item in sklFeatures:
        score = 0
        for (v, f) in zip(vars, sklFeatures[item]):
            score += v * f
        scores[item] = score
        if score < min: min = score
    # scores negativos estão sendo ignorados, para que isso não ocorra,
    # estou acrescentando o valor mínimo, assim score será sempre >= 0
    # e serão contabilizados no calculo de acurácia.
    if min < 0:
        min = abs(min)
        for i in scores: scores[i] += min
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def computeDistance(p1, p2):
    return abs(distance.euclidean(p1, p2))


def selectSolutions(file, user, userWeights, sklFeatures):
    global thresholdValue, distanceModel, noveltyModel
    arqVar = open(file, 'r')
    arqFun = open(file.replace('VAR', 'FUN'), 'r')
    selByDist = (float('inf'), '')
    for (vars, funs) in zip(arqVar, arqFun):
        vars = vars.strip()
        varValues = vars.split()
        varValues = [ float(v) for v in varValues ]
        funValues = funs.strip().split()
        funValues = [ abs(float(v)) for v in funValues ]
        usr_rank = computeScores(varValues, sklFeatures)
        noveltyModel.evaluationStart(user)
        utilityMetric = AccuracyUtilityMetric(thresholdValue)
        accuracyBias = calcUtility(utilityMetric, usr_rank)
        utilityMetric = DiversityUtilityMetric(distanceModel, usr_rank)
        diversityBias = calcUtility(utilityMetric, usr_rank)
        utilityMetric = NoveltyUtilityMetric(noveltyModel)
        noveltyBias = calcUtility(utilityMetric, usr_rank)
        # Caso hava erro no cálculo, utiliza o resultado geral:
        if math.isnan(accuracyBias): accuracyBias = funValues[0]
        if math.isnan(noveltyBias): noveltyBias = funValues[1]
        if math.isnan(diversityBias): diversityBias = funValues[2]
        sumBias = accuracyBias + diversityBias + noveltyBias
        solWeights = [ accuracyBias / sumBias, diversityBias / sumBias, noveltyBias / sumBias ]
        dist = computeDistance(userWeights, solWeights)
        if dist < selByDist[0]: selByDist = (dist, vars)
    arqVar.close()
    arqFun.close()
    return selByDist[1]


def processFile(file):
    print(f'file: {os.path.basename(file)}')
    if 'HR' in file:  hybrid = 'HR'
    elif 'STREAM' in file: hybrid = 'STREAM'
    else: hybrid = 'FWLS'
    fSel = '-all' not in file
    outfileDist = open(f'{file.replace("VAR.tsv", outfileName)}.csv', 'w')
    for user in usersWeights:
        sklFeatures = readSklFeatures(scikitFolder, user, hybrid, fSel)
        weightsDist = selectSolutions(file, user, usersWeights[user], sklFeatures)
        outfileDist.write(f'{user};{weightsDist}\n')
    outfileDist.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    homeDir         = sys.argv[1] # Bookcrossing
    featureMapsFile = sys.argv[2] # u.item.attributes
    thresholdValue  = float(sys.argv[3]) # 0 -- não avaliaremos apenas itens relevantes para obter a importância de acurácia
    ratingsFile     = sys.argv[4] # Sample1234.txt
    userWeightsFile = sys.argv[5] # Sample1234-sortedByRating_BIAS_1.txt
    searchFolder    = f'{homeDir}/{sys.argv[6]}' # MO-EPD_Rating_Run_R-1/F1234-5
    scikitFolder    = f'{homeDir}/{sys.argv[7]}' # Scikit-STREAM-EPD/F1234-5
    qtdThreads      = int(sys.argv[8])
    outfileName     = sys.argv[9] # padrão para salvar soluções escolhidas para cada usuário
    print('- reading features.')
    featureMaps = read.readFeatures.read("%s/BD/%s" % (homeDir, featureMapsFile))
    print('- reading ratings.')
    ratings = read.readRecommendation.read("%s/BD/%s" % (homeDir, ratingsFile))
    print('- creating distance model.')
    distanceModel = CosineFeatureItemDistanceModel(featureMaps[0], featureMaps[1])
    print('- creating novelty model.')
    noveltyModel = UserPCItemNovelty(ratings)
    print('- reading user\'s preferences.')
    usersWeights = readPreferences(f'{homeDir}/BD/{userWeightsFile}')
    print('- selecting solutions.')
    files = glob.glob(f'{searchFolder}/*E-true*-VAR.tsv')
    files = [ f for f in files if '-seq_' not in f ]
    executor = concurrent.futures.ThreadPoolExecutor(qtdThreads)
    futures = [ executor.submit(processFile, file) for file in files ]
    concurrent.futures.wait(futures)
    print("Fim")

'''
Calculate the scores from MO methods for baselines.

Created on 01/04/2017
Updated on 22/09/2017
           25/02/2019
@author: reifortes

Execution line: python3.4 ...
'''

import os, sys, glob


def readWeigths(file, ind):
    global weightsPath
    weightsFile = open(file, 'r')
    if ind:
        weights = {}
        for line in weightsFile:
            line = line.strip().split(';')
            id = int(line[0])
            weights[id] = [ float(x) for x in line[1].strip().split() ]
    else:
        weights = [ float(x) for x in weightsFile.readline().strip().split(' ') ]
    weightsFile.close()
    return weights


def computeScore(features, weights):
    score = 0
    for f, feature in enumerate(features):
        score += float(feature.split(':')[1]) * weights[f]
    return score


def processPredictions(file):
    global predictionDir, sklFileName, keysFileName
    print("Processing: %s" % (file))
    ind = '-ind-' in file.lower()
    weights = readWeigths(file, ind)
    outFileName = os.path.basename(file).replace('.csv', '.tsv')
    outfile = open('%s%s' % (predictionDir, outFileName), 'w')
    featuresFile = open(sklFileName, 'r')
    keysFile = open(keysFileName, 'r')
    for features, keys in zip(featuresFile, keysFile):
        features = features.strip().split()[1:]
        if ind:
            id = int(keys.strip().split(',')[0])
            if id not in weights: continue
            score = computeScore(features, weights[id])
        else:
            score = computeScore(features, weights)
        if score is None: continue
        outfile.write('%s\t%.6f\n' % ('\t'.join(keys.strip().split(',')), score))
    outfile.close()


if __name__ == '__main__':
    print("Inicio")
    homePath       = sys.argv[1]
    weightsPath    = homePath + sys.argv[2]
    solutionFile   = sys.argv[3]
    featuresPath   = homePath + sys.argv[4]
    sklFileName    = featuresPath + sys.argv[5]
    keysFileName   = featuresPath + sys.argv[6]
    predictionDir  = homePath + sys.argv[7]
    files = glob.glob('%s*%s*' % (weightsPath, solutionFile))
    for file in files:
        if ("HR-all"     in sklFileName) and not ("HR-all"     in file): continue
        if ("FWLS-all"   in sklFileName) and not ("FWLS-all"   in file): continue
        if ("STREAM-all" in sklFileName) and not ("STREAM-all" in file): continue
        if ("HR-sel"     in sklFileName) and not ("HR-sel"     in file): continue
        if ("FWLS-sel"   in sklFileName) and not ("FWLS-sel"   in file): continue
        if ("STREAM-sel" in sklFileName) and not ("STREAM-sel" in file): continue
        processPredictions(file)
    print("Fim")

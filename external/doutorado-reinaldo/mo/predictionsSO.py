'''
Calculate the scores from MO methods for baselines.

Created on 01/04/2017
Updated on 22/09/2017
           25/02/2019
@author: reifortes

Execution line: python3.4 ...
'''

import os,sys

def readNotBiasedWeigths(file):
    weightsFile = open('%s%s' % (weightsPath, file), 'r')
    weights = [ float(x) for x in weightsFile.readline().strip().split(' ') ]
    weightsFile.close()
    return weights


def computeNotBiasedScore(features, weights):
    score = 0
    for f, feature in enumerate(features):
        score += float(feature.split(':')[1]) * weights[f]
    return score


def processPredictions(file):
    print("Processing: %s" % (file))
    global weightsPath, predictionDir, featuresFile, keysFile
    weights = readNotBiasedWeigths(file)
    outFileName = os.path.basename(file).replace('.tsv', '')
    outfile = open('%s%s.tsv' % (predictionDir, outFileName.replace('-VAR', '')), 'w')
    fFile = open(featuresFile, 'r')
    kFile = open(keysFile, 'r')
    for features, keys in zip(fFile, kFile):
        features = features.strip().split()[1:]
        score = computeNotBiasedScore(features, weights)
        if score is None: continue
        outfile.write('%s\t%.6f\n' % ('\t'.join(keys.strip().split(',')), score))
    outfile.close()


if __name__ == '__main__':
    print("Inicio")
    homePath       = sys.argv[1]
    weightsPath    = homePath + sys.argv[2]
    featuresFileName = sys.argv[3]
    featuresPath   = homePath + sys.argv[4]
    keysFileName   = sys.argv[5]
    predictionDir  = homePath + sys.argv[6]
    featuresFile = f'{featuresPath}{featuresFileName}'
    keysFile = f'{featuresPath}{keysFileName}'
    files = [ s for s in os.listdir(weightsPath) if ('-VAR.tsv' in s and '-seq_' not in s) ]
    for file in files:
        if ("HR-all"     in featuresFileName and not "HR-all"     in file): continue
        if ("FWLS-all"   in featuresFileName and not "FWLS-all"   in file): continue
        if ("STREAM-all" in featuresFileName and not "STREAM-all" in file): continue
        if ("HR-sel"     in featuresFileName and not "HR-sel"     in file): continue
        if ("FWLS-sel"   in featuresFileName and not "FWLS-sel"   in file): continue
        if ("STREAM-sel" in featuresFileName and not "STREAM-sel" in file): continue
        processPredictions(file)
    print("Fim")

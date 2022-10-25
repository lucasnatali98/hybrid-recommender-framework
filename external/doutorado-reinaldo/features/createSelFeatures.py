'''
Obtem as features selecionadas e cria o arquivo skl

Created on 27/06/2019
Updated on
@authors: reifortes

'''


import sys, glob
sys.path.insert(0, '/Users/reifortes/Downloads/temp/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


def readFeatures(fileName):
    file = open(fileName, 'r')
    names = []
    for line in file:
        line = line.strip().split(' ')
        names.append(line[1].replace('.txt', ''))
    return names


def getMetrics(file, pattern):
    for line in file:
        if line.startswith(pattern):
            metrics = line.split('[')[1][0:-2].replace("'", "").split(', ')
            return set(metrics)
    return set()


def readDropedFeatures(filePattern):
    files = glob.glob(filePattern)
    droped = set()
    for fileName in files:
        file = open(fileName, 'r')
        droped = droped.union(getMetrics(file, '- To Drop by Gini'))
        droped = droped.union(getMetrics(file, '- To Drop by Correlation'))
        droped = droped.union(getMetrics(file, '- To Drop by Regression'))
    return droped


def writeFile(nameIn, nameOut, features, droped):
    sklFileIn = open(nameIn, 'r')
    sklFileOut = open(nameOut, 'w')
    for line in sklFileIn:
        values = line.strip().split(' ')
        sklFileOut.write('%s' % values[0])
        f = 1
        for value in values[1:]:
            x = value.split(':')
            if features[int(x[0]) - 1] not in droped:
                sklFileOut.write(' %d:%s' % (f, x[1]))
                f += 1
        sklFileOut.write('\n')
    sklFileIn.close()
    sklFileOut.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    util.using("Inicio")
    homeDir = sys.argv[1]  # /Users/reifortes/Documentos/tese/Jester
    fold = sys.argv[2] # F1234-5
    scikitDir = '%s/%s/%s' % (homeDir, sys.argv[3], fold) # features
    fileIn = sys.argv[4] # FWLS
    features = readFeatures('%s/%s-all.features' % (scikitDir, fileIn))
    selFile = '%s/%s-all.sel' % (scikitDir, fileIn)
    droped = readDropedFeatures(selFile.replace(fold, 'F????-?'))
    featureFile = open(selFile.replace('-all.sel', '-sel.features'), 'w')
    f = 1
    for feature in features:
        if feature not in droped:
            featureFile.write('%d: %s\n' % (f, feature))
            f += 1
    featureFile.close()
    writeFile(selFile.replace('.sel', '.train'), selFile.replace('-all.sel', '-sel.train'), features, droped)
    writeFile(selFile.replace('.sel', '.test'), selFile.replace('-all.sel', '-sel.test'), features, droped)
    util.using("Término")
'''
The Decision Making Process - Baseline.

Created on 01/04/2017
Updated on
@author: reifortes

Execution line: python3.4 ...
'''
import os,sys
from scipy.stats import norm
import numpy as np
import math


def getGeoRisk(mat, alpha=5):
    ##### IMPORTANT
    # This function takes a matrix of number of rows as a number of queries, and the number of collumns as the number of systems.
    ##############
    numSystems = mat.shape[1]
    numQueries = mat.shape[0]
    Tj = np.array([0.0] * numQueries)
    Si = np.array([0.0] * numSystems)
    geoRisk = np.array([0.0] * numSystems)
    zRisk = np.array([0.0] * numSystems)
    mSi = np.array([0.0] * numSystems)
    for i in range(numSystems):
        Si[i] = np.sum(mat[:, i])
        mSi[i] = np.mean(mat[:, i])
    for j in range(numQueries):
        Tj[j] = np.sum(mat[j, :])
    N = np.sum(Tj)
    for i in range(numSystems):
        tempZRisk = 0
        for j in range(numQueries):
            eij = Si[i] * (Tj[j] / N)
            xij_eij = mat[j, i] - eij
            if eij != 0:
                ziq = xij_eij / math.sqrt(eij)
            else:
                ziq = 0
            if xij_eij < 0:
                ziq = (1 + alpha) * ziq
            tempZRisk = tempZRisk + ziq
        zRisk[i] = tempZRisk
    c = numQueries
    for i in range(numSystems):
        ncd = norm.cdf(zRisk[i] / c)
        geoRisk[i] = math.sqrt((Si[i] / c) * ncd)
    return geoRisk


def georiskSelection(arqSol):
    global alpha
    solutions = [ ]
    for line in arqSol:
        numbers = [ abs(float(x)) for x in line.strip().split(' ') ]
        solutions.append(numbers)
    geoRisk = getGeoRisk(np.array(solutions).T, alpha)
    selMean = float("-inf")
    selLine = 0
    for l in range(len(geoRisk)):
        if geoRisk[l] > selMean:
            selMean = geoRisk[l]
            selLine = l
    return selLine


def meanSelection(arqSol):
    global objWeights, sumObjWeights
    selMean = float("-inf")
    selLine = 0
    for l, line in enumerate(arqSol):
        numbers = [ abs(float(x)) for x in line.strip().split(' ') ]
        mean = sum(n * w for n, w in zip(numbers, objWeights)) / sumObjWeights
        if mean > selMean:
            selMean = mean
            selLine = l
    return selLine


def selectSolution(arqSol):
    global objWeights
    return meanSelection(arqSol) if objWeights else georiskSelection(arqSol)


def processFile(file):
    print("- processing file: %s" % file)
    global homeDir, outfileName
    fileName = '%s/%s' % (homeDir, file)
    arqSol = open(fileName, 'r')
    sol = selectSolution(arqSol)
    arqSol.close()
    arqWeight = open(fileName.replace('PF-FUN.tsv', 'PF-VAR.tsv'), 'r')
    # pegar uma linha especifica para arquivos maiores:
    #   import linecache
    #   linecache.getline('/etc/passwd', 4)
    # mas, para arquivos pequenos:
    weights = []
    for i, line in enumerate(arqWeight):
        if i == sol:
            weights = line.strip()
            break
    arqWeight.close()
    # saving solution
    outfile = open(fileName.replace('PF-FUN.tsv', outfileName+'.csv'), 'w')
    outfile.write('%s\n' % (weights))
    outfile.close()


def processFolder():
    print("Processing folder.")
    global homeDir
    files = [ s for s in os.listdir(homeDir) if ('-PF-FUN.tsv' in s and '-seq_' not in s and not s.startswith('SO_')) ]
    for file in files:
        processFile(file)


if __name__ == '__main__':
    print("Inicio")
    homeDir     = sys.argv[1]
    alpha       = float(sys.argv[2])
    objWeights  = [ float(x) for x in sys.argv[3].split(";") ] if sys.argv[3] != '' else None
    outfileName = sys.argv[4]
    sumObjWeights = sum(objWeights) if objWeights else 0
    processFolder()
    print("Fim")

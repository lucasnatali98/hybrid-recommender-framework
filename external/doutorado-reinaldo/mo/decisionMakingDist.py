'''
The Decision Making Process - Baseline.

Created on 01/04/2017
Updated on
@author: reifortes

Execution line: python3.4 ...
'''
import os, sys, csv
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


def processFile(file):
    print("- processing file: %s" % file)
    global homeDir, outfileName, usersWeights
    fileName = '%s/%s' % (homeDir, file)
    arqVar = open(fileName.replace('FUN', 'VAR'), 'r')
    arqFun = open(fileName, 'r')
    userSelections = {}
    for uid in usersWeights:
        userSelections[uid] = (float('inf'), '')
    for (vars, funs) in zip(arqVar, arqFun):
        vars = vars.strip()
        funValues = funs.strip().split()
        funValues = [abs(float(v)) for v in funValues]
        accuracyBias = funValues[0]
        noveltyBias = funValues[1]
        diversityBias = funValues[2]
        sumBias = sum(funValues)
        if sumBias != 0:
            solWeights = [accuracyBias / sumBias, diversityBias / sumBias, noveltyBias / sumBias]
            for uid in usersWeights:
                dist = abs(distance.euclidean(usersWeights[uid], solWeights))
                if dist < userSelections[uid][0]: userSelections[uid] = (dist, vars)
    arqVar.close()
    arqFun.close()
    outfile = open(fileName.replace('PF-FUN.tsv', outfileName+'.csv'), 'w')
    for uid in userSelections:
        outfile.write(f'{uid};{userSelections[uid][1]}\n')
    outfile.close()


def processFolder(homeDir, qtdThreads):
    print("Processing folder.")
    files = [ s for s in os.listdir(homeDir) if ('-PF-FUN.tsv' in s and '-seq_' not in s and not s.startswith('SO_')) ]
    #executor = concurrent.futures.ThreadPoolExecutor(qtdThreads)
    #futures = [executor.submit(processFile, file) for file in files]
    #concurrent.futures.wait(futures)
    for file in files: processFile(file)


if __name__ == '__main__':
    print("Inicio")
    dataset         = sys.argv[1]
    homeDir         = f'{dataset}/{sys.argv[2]}'
    userWeightsFile = f'{dataset}/BD/{sys.argv[3]}'
    qtdThreads      = int(sys.argv[4])
    outfileName     = sys.argv[5]
    usersWeights    = readPreferences(userWeightsFile)
    processFolder(homeDir, qtdThreads)
    print("Fim")

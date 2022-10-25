'''
reifortes$
'''

import sys, glob
from shutil import move
from os import remove
from scipy.spatial import distance


def readWeights(dataSet, fold):
    data = {}
    file = open(f'{dataSet}/Results/Weights/{dataSet}-F{fold}_Accuracy_Weights.tsv', 'r')
    for line in file:
        line = line.strip().split()
        id = int(line[0])
        # cuidado, nos pesos há uma inversao na ordem dos obj
        acc = float(line[1])
        div = float(line[2])
        nov = float(line[3])
        data[id] = (acc, nov, div)
    file.close()
    return data


def computeDistance(p1, p2):
    return abs(distance.euclidean(p1, p2))


def processFile(filename, weights):
    move(filename, filename+'.old')
    old = open(filename+'.old', 'r')
    new = open(filename, 'w')
    # header
    line = old.readline().strip()
    new.write(f'{line}\tdist\tdist_risk\n')
    # data
    for line in old:
        try:
            line = line.strip()
            values = line.strip().split()
            id = abs(int(values[0]))
            acc = float(values[1])
            nov = float(values[2])
            div = float(values[3])
            s = acc + nov + div
            w = (acc/s, nov/s, div/s)
            dist1 = computeDistance(weights[id], w)
            risk_acc = float(values[4])
            risk_nov = float(values[5])
            risk_div = float(values[6])
            s = risk_acc + risk_nov + risk_div
            w = (risk_acc/s, risk_nov/s, risk_div/s)
            dist2 = computeDistance(weights[id], w)
            new.write(f'{line}\t{dist1:.10f}\t{dist2:.10f}\n')
        except:
            continue
    old.close()
    new.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    dataSet        = sys.argv[1]
    resultsFold    = f'{dataSet}/{sys.argv[2]}'
    fold           = sys.argv[3]
    topN           = sys.argv[4]
    weights = readWeights(dataSet, fold)
    # Reverter
    files = glob.glob(f'{resultsFold}/F????-{fold}/N{topN}/users/*.tsv.old')
    for oldFile in files:
        newFile = oldFile.replace('.tsv.old', '.tsv')
        remove(newFile)
        move(oldFile, newFile)
    # Processar
    files = glob.glob(f'{resultsFold}/F????-{fold}/N{topN}/users/*.tsv')
    for filename in files:
        print(f'File: {filename}')
        processFile(filename, weights)
    print("Término")

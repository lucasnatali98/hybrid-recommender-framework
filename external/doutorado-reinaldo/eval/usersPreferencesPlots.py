'''
Created on 29/02/2020
Updated on
@author: reifortes
'''

import sys, os, math
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
plt.style.use('grayscale')
plt.switch_backend('agg')
import pandas as pd
import numpy as np

folds = [
    ("2345" , "1"), #F1
    ("1345" , "2"), #F2
    ("1245" , "3"), #F3
    ("1235" , "4"), #F4
    ("1234" , "5"), #F5
]


def readUsers(testFile):
    users = set()
    file = open(testFile, 'r')
    for line in file:
        line = line.strip().replace('.0', '').split()
        uid = int(line[0])
        users.add(uid)
    return users


def readWeights(homePath, f, testUsers, allValues):
    values = []
    file = open('%s/BD/Sample%s.preferences' % (homePath, folds[f][1]), 'r')
    for line in file:
        line = line.strip().split()
        id = int(line[0])
        if id not in testUsers: continue
        acc = float(line[1])
        div = float(line[2])
        nov = float(line[3])
        if math.isnan(acc) or math.isnan(div) or math.isnan(nov): continue
        s = acc + div + nov
        values.append( (acc/s, div/s, nov/s, id) )
        allValues.append( (acc/s, div/s, nov/s, id) )
    file.close()
    return values


def plot2D(outFileName, x, f1, eild, epc):
    fig, ax = plt.subplots()
    ax.plot(x, f1, label='Accuracy', marker=".")
    ax.plot(x, epc, label='Novelty', marker=">")
    ax.plot(x, eild, label='Diversity', marker="<")
    ax.legend()
    plt.yticks(np.arange(0.1, 0.62, 0.1))
    plt.savefig(outFileName, bbox_inches="tight", pad_inches=0.0)
    plt.close('all')


def description(outFileName, descData):
    desc = descData.describe()
    desc.to_csv(outFileName, sep='\t')


def descrData(outFileName, f1, eild, epc):
    descData = {
        'Measures': pd.Series(['Accuracy', 'Diversity', 'Novelty']),
        'Accuracy': pd.Series(f1),
        'Diversity': pd.Series(eild),
        'Novelty': pd.Series(epc),
    }
    descData = pd.DataFrame(descData)
    description(outFileName, descData)


def saveWeights(outFileName, acc, div, nov, id):
    file = open(outFileName, 'w')
    for i in range(len(id)):
        file.write(f'{id[i]}\t{acc[i]}\t{div[i]}\t{nov[i]}\n')
    file.close()


def processObjWeights(homePath, outPath, f, values, metric):
    acc = [ e[0] for e in values ]
    div = [ e[1] for e in values ]
    nov = [ e[2] for e in values ]
    id = [e[3] for e in values]
    prefix = homePath.split('/')[-1]
    x = list(range(0, len(acc)))
    if not os.path.isdir(f'{outPath}'): os.makedirs(f'{outPath}')
    if f != None:
        plot2D(f'{outPath}/{prefix}-F{f+1}_{metric}_Weights_2D.pdf', x, acc, div, nov)
        descrData(f'{outPath}/{prefix}-F{f+1}_{metric}_Weights_Stats.tsv', acc, div, nov)
        saveWeights(f'{outPath}/{prefix}-F{f+1}_{metric}_Weights.tsv', acc, div, nov, id)
    else:
        plot2D(f'{outPath}/{prefix}-ALL_{metric}_Weights_2D.pdf', x, acc, div, nov)
        descrData(f'{outPath}/{prefix}-ALL_{metric}_Weights_Stats.tsv', acc, div, nov)
        saveWeights(f'{outPath}/{prefix}-ALL_{metric}_Weights.tsv', acc, div, nov, id)


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    homePath = sys.argv[1] # Bookcrossing
    outPath = f'{homePath}/Results/{sys.argv[2]}' # Plots
    allValues = []
    for f in range(0, 5):
        testUsers = readUsers(f'{homePath}/BD/Sample{folds[f][1]}.test')
        values = readWeights(homePath, f, testUsers, allValues)
        processObjWeights(homePath, outPath, f, sorted(values, key=lambda e: e[0]), 'Accuracy')
        processObjWeights(homePath, outPath, f, sorted(values, key=lambda e: e[1]), 'Diversity')
        processObjWeights(homePath, outPath, f, sorted(values, key=lambda e: e[2]), 'Novelty')
    processObjWeights(homePath, outPath, None, sorted(allValues, key=lambda e: e[0]), 'Accuracy')
    processObjWeights(homePath, outPath, None, sorted(allValues, key=lambda e: e[1]), 'Diversity')
    processObjWeights(homePath, outPath, None, sorted(allValues, key=lambda e: e[2]), 'Novelty')
    print("Término")

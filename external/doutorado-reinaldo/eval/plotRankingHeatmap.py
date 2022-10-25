'''
Plota gráfico de calor com os ranking dos algoritmos.

O arquivo tsv de entrada é resultado da execução do ranking (rankAlgorithms.py).

Feito para o ranking completo, com todas as métricas

reifortes$
'''

import sys, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from util import measures
from methods import Methods


def getValue(value):
    return float(value.replace(',', '.'))


def readRanking(file):
    data = {}
    infile = open(file, 'r')
    infile.readline() # cabecalho 1
    infile.readline() # cabecalho 2
    bestRank = float('inf')
    for line in infile:
        line = line.strip().split()
        method = line[0]
        rankNDCG = getValue(line[3])
        rankEPD = getValue(line[6])
        rankEILD = getValue(line[9])
        rankRiskNDCG = getValue(line[12])
        rankRiskEPD = getValue(line[15])
        rankRiskEILD = getValue(line[18])
        rankOverall = getValue(line[19])
        if rankOverall < bestRank: bestRank = rankOverall
        data[method] = [ rankNDCG, rankEPD, rankEILD, rankRiskNDCG, rankRiskEPD, rankRiskEILD, rankOverall ]
    infile.close()
    return data, bestRank


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    home   = sys.argv[1]
    basePath  = f'{home}/{sys.argv[2]}'
    inputFile = f'{basePath}/{sys.argv[3]}'
    outPath = f'{home}/{sys.argv[4]}'
    outFile = f'{outPath}/{sys.argv[5]}'
    if not os.path.exists(outPath): os.makedirs(outPath)
    data, bestRank = readRanking(inputFile)
    methods = Methods(fileName=inputFile)
    plotData = []
    xLabels = []
    lastCat = None
    for method in methods.methods:
        if lastCat != method.category:
            lastCat = method.category
            countCat = 1
        plotData.append(data[method.name][:-1])
        best = '$\\bigstar$' if bestRank == data[method.name][-1] else ''
        #xLabels.append(method.name)
        xLabels.append(f'{best}{method.category}-{countCat:02d}')
        countCat += 1
    plotData = np.array(plotData).transpose()
    plt.rcParams.update({'font.size': 8})
    fig, ax = plt.subplots()
    im = ax.imshow(plotData, cmap='gray')

    yLabels = measures #+ [ 'Overall' ]
    ax.set_yticks(np.arange(len(yLabels)))
    ax.set_yticklabels(yLabels)

    ax.set_xticks(np.arange(len(xLabels)))
    ax.set_xticklabels(xLabels)
    plt.xticks(rotation=90)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.07)
    plt.colorbar(im, cax=cax)

    #ax.set_title(home.split('/')[-2])
    fig.tight_layout()
    plt.savefig(outFile)
    plt.close()
    print("Término")

'''
Para salvar vários plots em um único PDF:
https://www.delftstack.com/pt/howto/matplotlib/how-to-save-plots-as-pdf-file-in-matplotlib/
'''
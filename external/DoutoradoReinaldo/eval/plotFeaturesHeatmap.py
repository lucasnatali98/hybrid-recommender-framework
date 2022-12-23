'''
Plota gráfico de calor com os pesos de metafeatures definidos pelos algoritmos.

O arquivo tsv de entrada é resultado da execução do ranking (rankAlgorithms.py).

Feito para o ranking completo, com todas as métricas

reifortes$
'''
import glob
import sys, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from util import measures
from methods import Methods
from util import getAlgName


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
        rankOverall = getValue(line[19])
        if rankOverall < bestRank: bestRank = rankOverall
        data[method] = rankOverall
    infile.close()
    return data, bestRank


def getFold(file):
    if   'F1234-5' in file: return 'F5'
    elif 'F1235-4' in file: return 'F4'
    elif 'F1245-3' in file: return 'F3'
    elif 'F1345-2' in file: return 'F2'
    elif 'F2345-1' in file: return 'F1'


def readCoefData(home, hybrid):
    files = sorted(glob.glob(f'{home}/MO/F*/R1/*{hybrid}*E-false_S-false*-SOL-*.csv'), reverse=True)
    files += sorted(glob.glob(f'{home}/SO/F*/R1/*{hybrid}*E-false*-VAR.tsv'), reverse=True)
    if hybrid == 'FWLS': files += sorted(glob.glob(f'{home}/Predictions/hybrid/R1/F*/{hybrid}*.coef'), reverse=True)
    files = [ f for f in files if not ('RISK' in f or '-Ind-' in f or '-GeoRisk' in f or '-sel' in f or '-seq' in f) ]
    coefs = []
    for file in files:
        algName = getAlgName(file).split('-')[0]
        fold = getFold(file)
        file = open(file, 'r')
        values = file.readline().replace('coef_	', '').strip().split()
        values = [ float(v) for v in values ]
        coefs.append([ f'{algName}-{fold}', values ])
        file.close()
    return coefs


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    home   = sys.argv[1] # Bookcrossing
    hybrid = sys.argv[2] # FWLS
    basePath  = f'{home}/{sys.argv[3]}' # Results/Analisys
    outPath = f'{home}/{sys.argv[4]}' # Results/Plots
    outFile = f'{outPath}/{sys.argv[5]}' # metafeatures_histogram_Bookcrossing.pdf
    if not os.path.exists(outPath): os.makedirs(outPath)
    coefData = readCoefData(home, hybrid)
    plotData = []
    yLabels = []
    for coef in coefData:
        plotData.append(coef[1])
        yLabels.append(coef[0])
    #plotData = np.array(plotData).transpose()
    plt.rcParams.update({'font.size': 5})
    fig, ax = plt.subplots()
    im = ax.imshow(plotData, cmap='gray')

    #yLabels = measures #+ [ 'Overall' ]
    ax.set_yticks(np.arange(len(yLabels)))
    ax.set_yticklabels(yLabels)

    #ax.set_xticks(np.arange(len(xLabels)))
    #ax.set_xticklabels(xLabels)
    #plt.xticks(rotation=90)

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
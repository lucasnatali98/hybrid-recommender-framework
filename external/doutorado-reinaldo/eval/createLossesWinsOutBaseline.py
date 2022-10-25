'''
Produces rankings for algorithms.
'''

# Avaliar Usuários segmentados:
# - Criar arquivos identificando os usuários para cada métrica (NDCG, EPD, EILD)
# -- abaixo da média / acima da média
# -- empates / vitória / derrota contra para Risk (IndSUM) em relação a mf-PEH (IndSUM)

import sys, glob
from util import folds
from util import getAlgName
from util import getAlgsRiskSort

# devem estar na ordem em que aparecem nos arquivos
measures = ['NDGC', 'EPD', 'EILD']


def readFromFile(fileName, filter, ignoreZeros):
    print(f'- readFromFile: {fileName}')
    file = open(fileName, 'r')
    rawData = {}
    file.readline()  # ignoring header
    for line in file:
        line = line.strip().replace(',', '.').replace('-', '')  # métricas negativadas para maximização no jMetal
        values = line.split()
        uid = int(values[0])
        values = [float(v) for v in values[1:4]]
        if ignoreZeros and values == [ 0.0, 0.0, 0.0 ]: continue
        rawData[uid] = values
    if filter == 1.0:
        users = set(rawData.keys())
    else:
        users = set()
        qtd = int(len(rawData)*filter)
        sel = sorted(rawData.items(), key=lambda x: x[1][0], reverse=False) # NDCG
        for k in range(qtd): users.add(sel[k][0])
        sel = sorted(rawData.items(), key=lambda x: x[1][1], reverse=False) # EPD
        for k in range(qtd): users.add(sel[k][0])
        sel = sorted(rawData.items(), key=lambda x: x[1][2], reverse=False) # EILD
        for k in range(qtd): users.add(sel[k][0])
    return rawData, users


def getData(riskPath, basePath, baseAlg, r1, r2, topn, filter, ignoreZeros):
    diffs = {}
    for r in range(r1, r2 + 1):
        for fold in folds:
            # baseline
            baselineValues, baselineKeys = readFromFile(glob.glob(f'{basePath}/R{r}/{fold}/N{topn}/users/{baseAlg}.tsv')[0], filter, ignoreZeros)
            # algoritmos
            files = glob.glob(f'{riskPath}/R{r}/{fold}/N{topn}/users/*.tsv')
            for file in files:
                alg = getAlgName(file)
                if alg not in diffs:
                    diffs[alg] = {}
                    diffs[alg]['loss_g_20'] = {}
                    for i in range(len(measures)): diffs[alg]['loss_g_20'][i] = 0
                algValues, algKeys = readFromFile(file, filter, ignoreZeros)
                for uid in algKeys:
                    if uid not in baselineKeys: continue
                    if uid not in diffs[alg]: diffs[alg][uid] = []
                    for i in range(len(measures)):
                        size_diff = algValues[uid][i] - baselineValues[uid][i]
                        if size_diff < 0:
                            p = ((size_diff * -1) * 100) / baselineValues[uid][i]
                            if p > 20: diffs[alg]['loss_g_20'][i] += 1
                        diffs[alg][uid].append(size_diff)
    return diffs


def processLossesWins(data):
    histogram = {}
    mean = {}
    for alg in data:
        histogram[alg] = {}
        mean[alg] = {}
        for m in measures: histogram[alg][m] = [0, 0]  # losses x wins
        for m in measures: mean[alg][m] = [0, 0]  # losses x wins
        for uid in data[alg]:
            if uid == 'loss_g_20': continue
            for m in range(len(measures)):
                if data[alg][uid][m] < 0:
                    histogram[alg][measures[m]][0] += 1
                    mean[alg][measures[m]][0] += abs(data[alg][uid][m])
                elif data[alg][uid][m] > 0:
                    histogram[alg][measures[m]][1] += 1
                    mean[alg][measures[m]][1] += data[alg][uid][m]
        for m in range(len(measures)):
            mean[alg][measures[m]][0] /= histogram[alg][measures[m]][0]
            mean[alg][measures[m]][1] /= histogram[alg][measures[m]][1]
    return histogram, mean


def saveFile(outFile, data, mean, diff):
    file = open(f'{outFile}.tsv', 'w')
    algs = getAlgsRiskSort(diff)
    algsStr = '\t\t'.join(algs)
    file.write(f'Criterion\tResult\t{algsStr}\n')
    for m in range(len(measures)):
        file.write(f'{measures[m]}\tWins')
        for alg in algs:
            losses = data[alg][measures[m]][0]
            wins = data[alg][measures[m]][1]
            if wins != 0:
                percent = 100 * (wins - losses) / losses
            else:
                percent = 0
            file.write((f'\t{wins}\t{percent:.4f}').replace('.', ','))
        file.write('\n\tLosses')
        for alg in algs:
            losses = data[alg][measures[m]][0]
            file.write(f'\t{losses}\t')
        file.write('\n\tImprovement')
        for alg in algs:
            degrad = mean[alg][measures[m]][0]
            improv = mean[alg][measures[m]][1]
            percent = 100 * (improv - degrad) / degrad
            file.write((f'\t{improv:.4f}\t{percent:.4f}').replace('.', ','))
        file.write('\n\tDegradation')
        for alg in algs:
            degrad = mean[alg][measures[m]][0]
            file.write((f'\t{degrad:.4f}\t').replace('.', ','))
        ####
        file.write('\n\tPerda > 20%')
        for alg in algs:
            d = diff[alg]['loss_g_20'][m]
            file.write((f'\t{d}\t').replace('.', ','))
        ####
        file.write('\n')
    file.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    home = sys.argv[1]
    riskPath = f'{home}/{sys.argv[2]}'
    basePath = f'{home}/{sys.argv[3]}'
    baseAlg = sys.argv[4]
    r1 = int(sys.argv[5])
    r2 = int(sys.argv[6])
    topn = sys.argv[7]
    filter = float(sys.argv[8])
    ignoreZeros = sys.argv[9].lower() in [ '1', 'true' ]
    outFile = f'{home}/{sys.argv[10]}'
    diff = getData(riskPath, basePath, baseAlg, r1, r2, topn, filter, ignoreZeros)
    data, mean = processLossesWins(diff)
    saveFile(outFile, data, mean, diff)
    print("Fim")

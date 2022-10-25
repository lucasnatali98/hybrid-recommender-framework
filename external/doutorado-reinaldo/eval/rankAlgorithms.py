'''
Produces rankings for algorithms.
'''

import sys, os, glob, numpy
from util import measures
from util import getAlgName
import time, random


def calculateIC(rawData, h):
    result = {}
    for measure in h:
        A = 0
        Q = 0
        k = 0
        for value in rawData[measure]:
            k += 1
            oldA = A
            A += (value - A) / k
            Q += (value - oldA) * (value - A)
        if k == 0:
            result[measure] = [ float('nan'), float('nan') ]
        elif k == 1:
            result[measure] = [ A, 0.0 ]
        else:
            std = numpy.sqrt(Q/(k-1))
            z = 1.96 # https://en.wikipedia.org/wiki/Confidence_interval
                     # http://www.dummies.com/education/math/statistics/checking-out-statistical-confidence-interval-critical-values/
            CI = z * (std / numpy.sqrt(k))
            result[measure] = [ A, CI ]
    return result


def getData(filePattern):
    global ignoreRisk, ignoreIndED, ignoreRisk
    files = glob.glob(filePattern)
    rawData = { }
    for fileName in files:
        alg = getAlgName(fileName)
        if ignoreRisk  and 'Risk' in alg: continue
        if ignoreIndED and ('Weighted' in alg or 'Stats' in alg): continue
        print(f'- getData: {fileName}\t{alg}')
        file = open(fileName, 'r')
        file.readline() # removendo o cabeçalho
        if alg not in rawData: rawData[alg] = { }
        igGeorisk = False
        for line in file:
            values = line.strip().split()
            for v in range(len(measures)):
                if igGeorisk and 'GeoRisk' in measures[v]: continue
                if measures[v] not in rawData[alg]: rawData[alg][measures[v]] = []
                rawData[alg][measures[v]].append(float(values[v+1].replace(',', '.').replace('-', ''))) # métricas negativadas para maximização no jMetal
            igGeorisk = True
    data = []
    for alg in rawData:
        if rawData[alg] == {}: continue
        icData = calculateIC(rawData[alg], measures)
        values = [ alg ]
        for measure in measures:
            values.append(icData[measure])
        data.append(values)
    return data


def rankData(data):
    global ignoreRiskMeasures
    print('- rankData')
    newData = [ d[:] for d in data ]
    for col in range(1, len(measures) + 1):
        print('-- sorting by ' + measures[col-1])
        newData.sort(key=lambda x: x[col][1], reverse=False) # IC sempre crescente
        if measures[col-1].startswith('Dist'):
            newData.sort(key=lambda x: x[col][0], reverse=False)  # distância deve ser minimizada, crescente
        else:
            newData.sort(key=lambda x: x[col][0], reverse=True) # métricas são maximizadas, decrescente
        num = 1
        qtd = 1
        indexDiscount = 0
        (value, ic) = (newData[0][col][0], newData[0][col][1])
        for index in range(1, len(newData)):
            (newValue, newIc) = (newData[index][col][0], newData[index][col][1])
            if measures[col - 1].startswith('Dist'):
                tie = ((value+ic)-(newValue-newIc) > 0)
            else:
                tie = ((value-ic)-(newValue+newIc) < 0)
            if not tie:
                (value, ic) = (newValue, newIc)
                rank = num / qtd
                for i in range(index-qtd, index):
                    newData[i][col].append(rank)
                num = index-indexDiscount+1
                qtd = 1
                if index == len(newData)-1:
                    rank = num / qtd
                    newData[index][col].append(rank)
            else:
                num += index-indexDiscount+1
                qtd += 1
                if index == len(newData)-1:
                    rank = num / qtd
                    for i in range(index-qtd+1, index+1):
                        newData[i][col].append(rank)
    for index in range(0, len(newData)):
        sumRanks = 0
        for col in range(1, len(measures) + 1):
            if ignoreRiskMeasures and 'GeoRisk' in measures[col-1]: continue
            sumRanks += newData[index][col][2]
        newData[index].append(sumRanks)
    newData.sort(key=lambda x: x[0], reverse=False)
    newData.sort(key=lambda x: x[-1], reverse=False)
    return newData


def writeSorted(arq, header, data, pareto):
    arq.write('Context\tAlgorithm\t')
    arq.write('\t'.join(header))
    arq.write('\n')
    for row in data:
        arq.write('\t'.join(str(v).replace('.', ',') for v in row))
        if pareto != None:
            arq.write('\t' + '\t'.join(pareto[row[0]]))
        arq.write('\n')


def saveFile(file, data):
    print('- saveFile: ' + file)
    arq = open(file, 'w')
    arq.write('Alg')
    for col in measures:
        arq.write(f'\t{col}\t\t')
    arq.write('\n')
    for col in measures:
        arq.write(f'\tMean\tIC\tRank')
    arq.write('\tOverall Ranking\n')
    for alg in data:
        arq.write(alg[0])
        for i in range(1, len(alg)-1):
            arq.write((f'\t{alg[i][0]}\t{alg[i][1]}\t{alg[i][2]}').replace('.', ','))
        arq.write((f'\t{alg[-1]}\n').replace('.', ','))
    arq.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    home = sys.argv[1]
    r1 = int(sys.argv[2])
    r2 = int(sys.argv[3])
    topn = sys.argv[4]
    outPath = f'{home}/Analisys'
    outFile = f'{outPath}/{sys.argv[5]}'
    ignoreRiskMeasures = len(sys.argv) >  6 and sys.argv[6]  == '1'
    ignoreRisk         = len(sys.argv) >  7 and sys.argv[7]  == '1'
    ignoreIndED        = len(sys.argv) >  8 and sys.argv[8]  == '1'
    segment            = '' if len(sys.argv) <=  9 else sys.argv[9]
    time.sleep(random.randint(0, 5))
    if not os.path.exists(outPath): os.makedirs(outPath)
    data = getData(f'{home}/R*{segment}/F*/N{topn}/users/*.tsv')
    rankedData = rankData(data)
    saveFile(f'{outFile}{segment}.tsv', rankedData)
    print("Fim")

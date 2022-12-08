'''
reifortes$
'''
import os.path
import sys, glob, math, subprocess
from scipy.spatial import distance
from util import getAlgName
from util import createPath
from util import StatsCalc


folds = [
    ("2345" , "1"), #F1
    ("1345" , "2"), #F2
    ("1245" , "3"), #F3
    ("1235" , "4"), #F4
    ("1234" , "5"), #F5
]


def readWeights(dataSet, fold):
    data = {}
    file = open(f'{dataSet}/Results/Weights/{dataSet}-F{fold}_Accuracy_Weights.tsv', 'r')
    for line in file:
        line = line.strip().split()
        id = int(line[0])
        acc = float(line[1])
        div = float(line[2])
        nov = float(line[3])
        data[id] = [acc, nov, div] # há uma inversão das métricas [NDCG, EPD, EILD]
    file.close()
    return data


def readUsersFront(front, dataSet, fold, type):
    users = set()
    file = open(f'{dataSet}/BD/Sample{fold}.{type}.test', 'r')
    for line in file:
        line = line.strip().split()
        id = int(line[0])
        users.add(id)
    file.close()
    data = []
    for id in front:
        if id in users: data.append(front[id])
    return data


def readParetoFront(fileName):
    file = open(fileName, 'r')
    points = []
    for line in file:
        if 'nan' in line: continue
        line = line.strip().replace(',', '.').split()
        metrics = [float(x) for x in line]
        acc = metrics[0]
        nov = metrics[1]
        div = metrics[2]
        sum = acc + nov + div
        try:
            points.append([ acc/sum, nov/sum, div/sum ])
        except:
            continue
    return points


def getSequence(fileName):
    #if '-seq_' in fileName: return int(fileName.replace('-PF-FUN.tsv', '').split('-seq_')[1])
    if '-seq_' in fileName: return int(fileName.replace('-FUN.tsv', '').split('-seq_')[1])
    else: return -1


def computeGD(approx, front):
    sum = 0
    for a in approx:
        min = float('inf')
        for f in front:
            dist = distance.euclidean(a, f)
            if dist < min: min = dist
        sum += min ** 2
    if len(approx) == 0: return float('inf')
    return math.sqrt(sum) / len(approx) # Lembrete: quanto menor melhor


def computeIGD(approx, front):
    return computeGD(front, approx)


def computeHV(fileName):
    result = subprocess.Popen(['run/eval/hv-1.3-src/hv', '-r 0 0 0', fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = result.communicate()
    try:
        valor = float(out.decode("utf-8").strip())
    except:
        valor = -1
    return valor


def updateData(data, algName, seq, approx, front):
    if algName not in data: data[algName] = {}
    if seq not in data[algName]: data[algName][seq] = {'gd': StatsCalc(), 'igd': StatsCalc()}
    gd = computeGD(approx, front)
    igd = computeIGD(approx, front)
    data[algName][seq]['gd'].update(gd)
    data[algName][seq]['igd'].update(igd)


def calculate():
    global dataSet, igRisk
    dataGD = { 'all': {}, 'top': {}, 'bot': {} }
    dataHV = {}
    for f in folds:
        train = f[0]
        test = f[1]
        front = readWeights(dataSet, test)
        topFront = readUsersFront(front, dataSet, test, 'top')
        botFront = readUsersFront(front, dataSet, test, 'bot')
        front = list(front.values())
        files = glob.glob(f'{dataSet}/PREF-6h/MO/F{train}-{test}/R1/*-PF-FUN.tsv')
        files.extend(glob.glob(f'{dataSet}/RANK-6h/MO/F{train}-{test}/R1/*-PF-FUN.tsv'))
        if not igRisk: files.extend(glob.glob(f'{dataSet}/RISK-6h/MO/F{train}-{test}/R1/*-PF-FUN.tsv'))
        for filename in files:
            #avaliando população, como feito no capitulo 3.
            filename = filename.replace('-PF-FUN.tsv', '-FUN.tsv')
            baseName = os.path.basename(filename)
            algName = getAlgName(baseName)
            if igRisk and '-Risk' in algName: continue
            seq = getSequence(baseName)
            print(f'File: {baseName} ({algName})')
            approx = readParetoFront(filename)
            updateData(dataGD['all'], algName, seq, approx, front)
            updateData(dataGD['top'], algName, seq, approx, topFront)
            updateData(dataGD['bot'], algName, seq, approx, botFront)
            hv = computeHV(filename)
            if algName not in dataHV: dataHV[algName] = {}
            if seq not in dataHV[algName]: dataHV[algName][seq] = {'HV': StatsCalc()}
            dataHV[algName][seq]['HV'].update(hv)
    return dataGD, dataHV


def rank(data, measures):
    newData = [ d[:] for d in data ]
    for col in range(1, len(measures) + 1):
        newData.sort(key=lambda x: x[col][1], reverse=False) # IC sempre crescente
        if measures[col-1] == 'HV': newData.sort(key=lambda x: x[col][0], reverse=True)  # HV, quanto maior melhor, decrescente
        else: newData.sort(key=lambda x: x[col][0], reverse=False)  # distância deve ser minimizada, crescente
        num = 1
        qtd = 1
        indexDiscount = 0
        (value, ic) = (newData[0][col][0], newData[0][col][1])
        for index in range(1, len(newData)):
            (newValue, newIc) = (newData[index][col][0], newData[index][col][1])
            if measures[col-1] == 'HV': tie = ((value-ic)-(newValue+newIc) < 0)
            else: tie = ((value + ic) - (newValue - newIc) > 0)
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
            sumRanks += newData[index][col][2]
        newData[index].append(sumRanks)
    newData.sort(key=lambda x: x[0], reverse=False)
    newData.sort(key=lambda x: x[-1], reverse=False)
    return newData


def saveFile(file, data, measures):
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
    dataSet = sys.argv[1]
    outFold = f'{dataSet}/{sys.argv[2]}'
    igRisk = True if (len(sys.argv) > 3 and sys.argv[3] == '1') else False
    extraExt = '.-risk' if igRisk else ''
    createPath(outFold)
    dataGD, dataHV = calculate()
    measures = [ 'GD', 'IGD' ]
    measuresHV = [ 'HV' ]
    for type in dataGD:
        measuresHV.append(f'{type}_GD')
        measuresHV.append(f'{type}_IGD')
        outFile = open(f'{outFold}/generationalDistances_Seq_{type}{extraExt}.tsv', 'w')
        outFile.write('Alg\tSeq\tGD\tIC\tIGD\tIC\n')
        rankData = []
        for algName in dataGD[type]:
            linha = [ algName ]
            for seq in dataGD[type][algName]:
                gd = dataGD[type][algName][seq]['gd'].calcIC()
                igd = dataGD[type][algName][seq]['igd'].calcIC()
                outFile.write(f'{algName}\t{seq}\t{gd[0]:.10f}\t{gd[1]:.10f}\t{igd[0]:.10f}\t{igd[1]:.10f}\n')
                if seq < 0:
                    linha.append(list(gd))
                    linha.append(list(igd))
                dataHV[algName][seq][f'{type}_GD'] = gd
                dataHV[algName][seq][f'{type}_IGD'] = igd
            rankData.append(linha)
        outFile.close()
        rankData = rank(rankData, measures)
        saveFile(f'{outFold}/generationalDistances_Rank_{type}{extraExt}.tsv', rankData, measures)
    rankData = []
    outFile = open(f'{outFold}/generationalDistances_Seq_HV{extraExt}.tsv', 'w')
    outFile.write('Alg\tSeq\tHV\tIC\n')
    for algName in dataHV:
        linha = [algName]
        for seq in dataHV[algName]:
            hv = dataHV[algName][seq]['HV'].calcIC()
            outFile.write(f'{algName}\t{seq}\t{hv[0]:.10f}\t{hv[1]:.10f}\n')
            if seq < 0:
                for m in measuresHV: linha.append(list(hv))
            dataHV[algName][seq]['HV'] = hv
        rankData.append(linha)
    outFile.close()
    rankData = rank(rankData, measuresHV)
    saveFile(f'{outFold}/generationalDistances_Rank_HV{extraExt}.tsv', rankData, measuresHV)
    print("Término")

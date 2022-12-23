'''

'''

# Avaliar Usuários segmentados:
# - Criar arquivos identificando os usuários para cada métrica (NDCG, EPD, EILD)
# -- abaixo da média / acima da média
# -- empates / vitória / derrota contra para Risk (IndSUM) em relação a mf-PEH (IndSUM)

import sys, glob
from statistics import mean
from util import folds
from util import getAlgName
from util import getAlgsRiskSort
import numpy as np
import scipy.stats as st

# devem estar na ordem em que aparecem nos arquivos
measures = ['NDGC', 'EPD', 'EILD']


def computeCI(data):
    ic = st.t.interval(alpha=0.95, df=len(data) - 1, loc=np.mean(data), scale=st.sem(data))
    i = (ic[1] - ic[0]) / 2
    return ic[0]+i, i


class Values:
    def __init__(self):
        self.losses = []
        self.wins = []
        self.ties = []
        self.loss_g_20 = []
        self.loss_g_30 = []
        self.loss_g_40 = []
        self.loss_g_50 = []
        self.loss_g_60 = []
        self.improvement = []
        self.degradation = []
        self.degradation_g_20 = []
        self.degradation_g_30 = []
        self.degradation_g_40 = []
        self.degradation_g_50 = []
        self.degradation_g_60 = []


class Results:
    def __init__(self):
        self.values = []
        for m in range(len(measures)):
            self.values.append(Values())
    def compute(self, computation):
        for m in range(len(measures)):
            self.values[m].losses.append(len(computation.computations[m].losses))
            self.values[m].wins.append(len(computation.computations[m].wins))
            self.values[m].ties.append(computation.computations[m].ties)
            self.values[m].loss_g_20.append(len(computation.computations[m].loss_g_20))
            self.values[m].loss_g_30.append(len(computation.computations[m].loss_g_30))
            self.values[m].loss_g_40.append(len(computation.computations[m].loss_g_40))
            self.values[m].loss_g_50.append(len(computation.computations[m].loss_g_50))
            self.values[m].loss_g_60.append(len(computation.computations[m].loss_g_60))
            if len(computation.computations[m].wins) == 0: self.values[m].improvement.append(0)
            else: self.values[m].improvement.append(mean(computation.computations[m].wins))
            if len(computation.computations[m].losses) == 0: self.values[m].degradation.append(0)
            else: self.values[m].degradation.append(mean(computation.computations[m].losses))
            if len(computation.computations[m].loss_g_20) == 0: self.values[m].degradation_g_20.append(0)
            else: self.values[m].degradation_g_20.append(mean((computation.computations[m].loss_g_20)))
            if len(computation.computations[m].loss_g_30) == 0: self.values[m].degradation_g_30.append(0)
            else: self.values[m].degradation_g_30.append(mean((computation.computations[m].loss_g_30)))
            if len(computation.computations[m].loss_g_40) == 0: self.values[m].degradation_g_40.append(0)
            else: self.values[m].degradation_g_40.append(mean((computation.computations[m].loss_g_40)))
            if len(computation.computations[m].loss_g_50) == 0: self.values[m].degradation_g_50.append(0)
            else: self.values[m].degradation_g_50.append(mean((computation.computations[m].loss_g_50)))
            if len(computation.computations[m].loss_g_60) == 0: self.values[m].degradation_g_60.append(0)
            else: self.values[m].degradation_g_60.append(mean((computation.computations[m].loss_g_60)))

    def getLosses(self, m):
        return computeCI(self.values[m].losses)
    def getWins(self, m):
        return computeCI(self.values[m].wins)
    def getTies(self, m):
        return computeCI(self.values[m].ties)
    def getLossG20(self, m):
        return computeCI(self.values[m].loss_g_20)
    def getLossG30(self, m):
        return computeCI(self.values[m].loss_g_30)
    def getLossG40(self, m):
        return computeCI(self.values[m].loss_g_40)
    def getLossG50(self, m):
        return computeCI(self.values[m].loss_g_50)
    def getLossG60(self, m):
        return computeCI(self.values[m].loss_g_60)
    def getImprovement(self, m):
        return computeCI(self.values[m].improvement)
    def getDegradation(self, m):
        return computeCI(self.values[m].degradation)
    def getDegradationG20(self, m):
        return computeCI(self.values[m].degradation_g_20)
    def getDegradationG30(self, m):
        return computeCI(self.values[m].degradation_g_30)
    def getDegradationG40(self, m):
        return computeCI(self.values[m].degradation_g_40)
    def getDegradationG50(self, m):
        return computeCI(self.values[m].degradation_g_50)
    def getDegradationG60(self, m):
        return computeCI(self.values[m].degradation_g_60)


class Computation:
    def __init__(self):
        self.losses = []
        self.wins = []
        self.ties = 0
        self.loss_g_20 = []
        self.loss_g_30 = []
        self.loss_g_40 = []
        self.loss_g_50 = []
        self.loss_g_60 = []
    def compute(self, algValue, baseValue):
        diff = algValue - baseValue
        if diff < 0:
            self.addLosses(diff)
            p = ((diff * -1) * 100) / baseValue
            if p > 20: self.addLossG20(diff)
            if p > 30: self.addLossG30(diff)
            if p > 40: self.addLossG40(diff)
            if p > 50: self.addLossG50(diff)
            if p > 60: self.addLossG60(diff)
        elif diff > 0:
            self.addWins(diff)
        else:
            self.ties += 1
    def addLosses(self, value):
        self.losses.append(abs(value))
    def addWins(self, value):
        self.wins.append(abs(value))
    def addLossG20(self, value):
        self.loss_g_20.append(abs(value))
    def addLossG30(self, value):
        self.loss_g_30.append(abs(value))
    def addLossG40(self, value):
        self.loss_g_40.append(abs(value))
    def addLossG50(self, value):
        self.loss_g_50.append(abs(value))
    def addLossG60(self, value):
        self.loss_g_60.append(abs(value))


class Computations:
    def __init__(self):
        self.computations = []
        self.ignored = 0
        for m in range(len(measures)):
            self.computations.append(Computation())
    def compute(self, algValues, algKeys, baselineValues, baselineKeys):
        for uid in algKeys:
            if uid not in baselineKeys:
                self.ignored += 1
                continue
            for m in range(len(measures)):
                self.computations[m].compute(algValues[uid][m], baselineValues[uid][m])


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
        if ignoreZeros and values == [0.0, 0.0, 0.0]: continue
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


def getResults(riskPath, r1, r2, topn, filter, ignoreZeros):
    results = {}
    for r in range(r1, r2 + 1):
        for fold in folds:
            files = glob.glob(f'{riskPath}/R{r}/{fold}/N{topn}/users/*.tsv')
            files = sorted(files)
            for f1 in files:
                alg1 = getAlgName(f1)
                alg1Values, alg1Keys = readFromFile(f1, filter, ignoreZeros)
                if alg1 not in results: results[alg1] = Results()
                for f2 in files:
                    comp = Computations()
                    alg2 = getAlgName(f2)
                    if alg1 == alg2: continue
                    alg2Values, alg2Keys = readFromFile(f2, filter, ignoreZeros)
                    comp.compute(alg1Values, alg1Keys, alg2Values, alg2Keys)
                    results[alg1].compute(comp)
    return results


def rankResults(results, reverse=False):
    results.sort(key=lambda x: x[2], reverse=False) # IC sempre crescente
    results.sort(key=lambda x: x[1], reverse=reverse)
    num = 1
    qtd = 1
    indexDiscount = 0
    (value, ic) = (results[0][1], results[0][2])
    for index in range(1, len(results)):
        (newValue, newIc) = (results[index][1], results[index][2])
        tie = ((value - ic) - (newValue + newIc) < 0)
        if not tie:
            (value, ic) = (newValue, newIc)
            rank = num / qtd
            for i in range(index - qtd, index): results[i].append(rank)
            num = index - indexDiscount + 1
            qtd = 1
            if index == len(results) - 1:
                rank = num / qtd
                results[index].append(rank)
        else:
            num += index - indexDiscount + 1
            qtd += 1
            if index == len(results) - 1:
                rank = num / qtd
                for i in range(index - qtd + 1, index + 1):
                    results[i].append(rank)
    ranked = {}
    for r in results:
        ranked[r[0]] = (r[1], r[2], r[3])
    return ranked


def writeResults(header, algs, results, method, m, reverse, file):
    file.write(header)
    ranked = []
    for alg in algs:
        val, ic = method(results[alg], m)
        ranked.append([alg, val, ic])
    ranked = rankResults(ranked, reverse)
    for alg in algs:
        # file.write((f'\t{ranked[alg][0]:.2f}\t{ranked[alg][1]:.4f}\t{ranked[alg][2]:.1f}').replace('.', ','))
        #file.write((f'\t{ranked[alg][0]:.2f}\t{ranked[alg][2]:.1f}').replace('.', ','))
        file.write((f'\t{ranked[alg][0]:.4f}').replace('.', ','))


def saveFile(outFile, results):
    file = open(f'{outFile}.tsv', 'w')
    algs = getAlgsRiskSort(results)
    #algsStr = '\t\t\t'.join(algs)
    #algsStr = '\t\t'.join(algs)
    algsStr = '\t'.join(algs)
    file.write(f'Criterion\tResult\t{algsStr}\n')
    for m in range(len(measures)):
        writeResults(f'{measures[m]}\tWins', algs, results, Results.getWins, m, True, file)
        writeResults('\n\tLosses', algs, results, Results.getLosses, m, False, file)
        #writeResults('\n\tTies', algs, results, Results.getTies, m, False, file)
        writeResults('\n\tImprovement', algs, results, Results.getImprovement, m, True, file)
        writeResults('\n\tDegradation', algs, results, Results.getDegradation, m, False, file)
        writeResults('\n\tLoss > 20%', algs, results, Results.getLossG20, m, False, file)
        writeResults('\n\tDegradation > 20%', algs, results, Results.getDegradationG20, m, False, file)
        writeResults('\n\tLoss > 30%', algs, results, Results.getLossG30, m, False, file)
        writeResults('\n\tDegradation > 30%', algs, results, Results.getDegradationG30, m, False, file)
        writeResults('\n\tLoss > 40%', algs, results, Results.getLossG40, m, False, file)
        writeResults('\n\tDegradation > 40%', algs, results, Results.getDegradationG40, m, False, file)
        writeResults('\n\tLoss > 50%', algs, results, Results.getLossG50, m, False, file)
        writeResults('\n\tDegradation > 50%', algs, results, Results.getDegradationG50, m, False, file)
        writeResults('\n\tLoss > 60%', algs, results, Results.getLossG60, m, False, file)
        writeResults('\n\tDegradation > 60%', algs, results, Results.getDegradationG60, m, False, file)
        file.write('\n')
    file.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    home = sys.argv[1]
    riskPath = f'{home}/{sys.argv[2]}'
    r1 = int(sys.argv[3])
    r2 = int(sys.argv[4])
    topn = sys.argv[5]
    filter = float(sys.argv[6])
    ignoreZeros = sys.argv[7].lower() in [ '1', 'true' ]
    outFile = f'{home}/{sys.argv[8]}'
    results = getResults(riskPath, r1, r2, topn, filter, ignoreZeros)
    saveFile(outFile, results)
    print("Fim")

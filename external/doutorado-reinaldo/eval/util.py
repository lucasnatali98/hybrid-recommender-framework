import os, numpy, time, random

measures = [ 'NDCG', 'EPD', 'EILD',
             'GeoRisk-NDCG', 'GeoRisk-EPD', 'GeoRisk-EILD',
             'Dist', 'Dist-GeoRisk' ]

folds = [ 'F2345-1', 'F1345-2', 'F1245-3', 'F1235-4', 'F1234-5' ]

def getAlgName(fileName):
    fileName = os.path.basename(fileName)
    sep = '-' # se mudar pode causar impacto em outros scripts...
    algName = ''
    # Constituent
    if 'ALS_' in fileName: return 'ALS'
    if 'BiasedMatrix' in fileName: return 'Biased-MF'
    if 'BiasedSVD' in fileName: return 'Biased-SVD'
    if 'TF_BiasedMF' in fileName: return 'TF_Biased-MF'
    if 'IntegratedBiasMF' in fileName: return 'IntegratedBias-MF'
    if 'Bias' in fileName: return 'Bias'
    if 'BiPolar' in fileName: return 'BP-SlopeOne'
    if 'cbpr' in fileName: return 'BPR'
    if 'ImplicitMF' in fileName: return 'Implicit-MF'
    if 'ItemKNN' in fileName: return 'ItemKNN'
    if 'UserKNN' in fileName: return 'UserKNN'
    if 'ncf' in fileName: return 'NCF'
    if 'SlopeOne' in fileName: return 'SlopeOne'
    if 'SVDPlusPlus' in fileName: return 'SVDPlusPlus'
    if 'CB_Lucene' in fileName: return 'CB-Lucene'
    # Hydrib
    if fileName.startswith('FWLS-all-'): return f'FWLS{sep}All'
    if fileName.startswith('FWLS-sel-'): return f'FWLS{sep}Sel'
    if fileName.startswith('HR-sel-'): return f'HR{sep}Sel'
    if fileName.startswith('HR-all-'): return f'HR{sep}All'
    if fileName.startswith('STREAM-sel-'): return f'STREAM{sep}Sel'
    if fileName.startswith('STREAM-all-'): return f'STREAM{sep}All'
    # MO Strategy
    if  fileName.startswith('SO_'): algName += f'SO{sep}Rank'
    elif fileName.startswith('MO_'): algName += f'MO{sep}Rank'
    elif fileName.startswith('RISK_SO_'): algName += f'SO{sep}Risk'
    elif fileName.startswith('RISK_MO_'): algName += f'MO{sep}Risk'
    elif fileName.startswith('FAIR_SO_'): algName += f'SO{sep}Fair'
    elif fileName.startswith('FAIR_MO_'): algName += f'MO{sep}Fair'
    # feature strategy
    if   'FWLS-' in fileName: algName += f'{sep}FWLS'
    elif 'HR-' in fileName: algName += f'{sep}HR'
    elif 'STREAM-' in fileName: algName += f'{sep}STREAM'
    # feature selection
    if '-all_' in fileName: algName += f'{sep}All'
    elif '-sel_' in fileName: algName += f'{sep}Sel'
    # Weighted or not
    if 'E-true' in fileName: algName += f'{sep}Weighted'
    #elif 'E-false' in fileName: algName += f'{sep}Standard'
    if algName.startswith('SO'): return algName
    # Statistical test relation
    if 'S-true' in fileName: algName += f'{sep}Stats'
    #elif 'S-false' in fileName: algName += f'{sep}Simple'
    # Decision strategy
    if   'Ind-GeoRisk' in fileName: algName += f'{sep}IndRisk'
    elif 'Ind-SUM' in fileName: algName += f'{sep}IndSUM'
    elif 'Ind-DIST' in fileName: algName += f'{sep}IndDIST'
    elif 'GeoRisk' in fileName: algName += f'{sep}Risk'
    elif 'SUM' in fileName: algName += f'{sep}SUM'
    return algName


def getAlgsRiskSort(algs):
    algsSort = {}
    for alg in algs:
        points = 0
        if alg.startswith('MO'):
            points += 1000
            if alg.startswith('MO-Risk'): points += 10000
            if alg.startswith('MO-Fair'): points += 5000
        elif alg.startswith('SO'):
            points += 500
            if alg.startswith('SO-Risk'): points += 9000
            if alg.startswith('SO-Fair'): points += 3000
        if alg.endswith('SingleSUM'): points += 40
        elif alg.endswith('SingleRisk'): points += 30
        if alg.endswith('IndSUM'): points += 20
        elif alg.endswith('IndRisk'): points += 10
        if 'FWLS-' in alg or 'STREAM-' in alg or 'HR-' in alg: points += 5
        algsSort[alg] = points
    return sorted(algsSort, key=algsSort.get, reverse=True)


def createPath(pathName):
    time.sleep(random.randint(0, 5))
    if not os.path.exists(pathName): os.makedirs(pathName)


class StatsCalc:
    A = None
    Q = None
    K = None
    z = 1.96 # 95% (http://www.dummies.com/education/math/statistics/checking-out-statistical-confidence-interval-critical-values/)
             # https://en.wikipedia.org/wiki/Confidence_interval
    def __init__(self, z=1.96):
        self.A = 0
        self.Q = 0
        self.K = 0
        self.z = z
    def update(self, value):
        self.K += 1
        oldA = self.A
        self.A = oldA + (value - oldA) / self.K
        self.Q += (value - oldA) * (value - self.A)
    def calcIC(self):
        if self.K <= 1: return (float('nan'), float('nan'))
        std = numpy.sqrt(self.Q/(self.K-1))
        CI = self.z * (std / numpy.sqrt(self.K))
        return (self.A, CI)
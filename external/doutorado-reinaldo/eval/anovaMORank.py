import os, sys, glob
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
from util import getAlgName
from util import createPath


Algoritmos = { 'Amazon':       { 'WHF': [ 'HR-All', 'HR-Sel', 'STREAM-All', 'STREAM-Sel' ],
                                 'SO':  [ 'SO-Rank-HR-All', 'SO-Rank-HR-Sel', 'SO-Rank-STREAM-All', 'SO-Rank-STREAM-Sel' ],
                                 'MO':  [ 'MO-Rank-HR-All-IndSUM', 'MO-Rank-HR-All-SUM', 'MO-Rank-HR-Sel-IndSUM', 'MO-Rank-HR-Sel-SUM',
                                          'MO-Rank-FWLS-All-IndSUM', 'MO-Rank-FWLS-All-SUM', 'MO-Rank-FWLS-Sel-IndSUM', 'MO-Rank-FWLS-Sel-SUM' ] },
               'Bookcrossing': { 'WHF': [ 'HR-All', 'HR-Sel', 'FWLS-All', 'FWLS-Sel' ],
                                 'SO':  [ 'SO-Rank-HR-All', 'SO-Rank-HR-Sel', 'SO-Rank-FWLS-All', 'SO-Rank-FWLS-Sel' ],
                                 'MO':  [ 'MO-Rank-HR-All-IndSUM', 'MO-Rank-HR-All-SUM', 'MO-Rank-HR-Sel-IndSUM', 'MO-Rank-HR-Sel-SUM',
                                          'MO-Rank-STREAM-All-IndSUM', 'MO-Rank-STREAM-All-SUM', 'MO-Rank-STREAM-Sel-IndSUM', 'MO-Rank-STREAM-Sel-SUM' ] },
               'Jester':       { 'WHF': [ 'HR-All', 'HR-Sel', 'FWLS-All', 'FWLS-Sel' ],
                                 'SO':  [ 'SO-Rank-HR-All', 'SO-Rank-HR-Sel', 'SO-Rank-FWLS-All', 'SO-Rank-FWLS-Sel' ],
                                 'MO':  [ 'MO-Rank-HR-All-IndSUM', 'MO-Rank-HR-All-SUM', 'MO-Rank-HR-Sel-IndSUM', 'MO-Rank-HR-Sel-SUM',
                                          'MO-Rank-STREAM-All-IndSUM', 'MO-Rank-STREAM-All-SUM', 'MO-Rank-STREAM-Sel-IndSUM', 'MO-Rank-STREAM-Sel-SUM' ] },
               'ML20M':        { 'WHF': [ 'HR-All', 'HR-Sel', 'FWLS-All', 'FWLS-Sel' ],
                                 'SO':  [ 'SO-Rank-HR-All', 'SO-Rank-HR-Sel', 'SO-Rank-FWLS-All', 'SO-Rank-FWLS-Sel' ],
                                 'MO':  [ 'MO-Rank-HR-All-IndSUM', 'MO-Rank-HR-All-SUM', 'MO-Rank-HR-Sel-IndSUM', 'MO-Rank-HR-Sel-SUM',
                                          'MO-Rank-STREAM-All-IndSUM', 'MO-Rank-STREAM-All-SUM', 'MO-Rank-STREAM-Sel-IndSUM', 'MO-Rank-STREAM-Sel-SUM' ] } }
Metricas = [ 'NDCG', 'EPD', 'EILD', 'risk_NDCG', 'risk_EPD', 'risk_EILD' ]
metricasStr = '\t'.join(Metricas)


def getLine(alg, line):
    data = []
    data.append('No' if 'HR-' in alg else 'Yes')
    data.append('No' if '-All' in alg else 'Yes')
    if alg.startswith('MO-'): data.append('Ind' if '-Ind' in alg else 'All')
    line = line.strip().replace(',', '.').replace('-', '').split()
    data.extend(line[1:])
    return '\t'.join(data)


def processFiles(algs, resultsHome, r1, r2, topN, outFold):
    for method in algs:
        print(f'- Processing {method}')
        outfile = open(f'{outFold}/{method}.tsv', 'w')
        if method == 'MO': outfile.write(f'MF\tSel\tDM\t{metricasStr}\n')
        else: outfile.write(f'MF\tSel\t{metricasStr}\n')
        for r in range(r1, r2+1):
            folds = glob.glob(f'{resultsHome}/R{r}/*')
            for fold in folds:
                files = glob.glob(f'{fold}/N{topN}/users/*.tsv')
                for file in files:
                    alg = getAlgName(os.path.basename(file))
                    if alg not in algs[method]: continue
                    file = open(file, 'r')
                    file.readline()
                    for line in file:
                        outfile.write(f'{getLine(alg, line)}\n')
        outfile.close()


def anova(formula, inFile, outFile):
    data = pd.read_csv(inFile, sep='\t')
    model = ols(formula, data=data).fit()
    table = sm.stats.anova_lm(model, typ=3)
    table.to_csv(outFile, sep='\t')


def computeAnova(outFold):
    for metric in Metricas:
        anova(f'{metric} ~ C(MF, Sum) * C(Sel, Sum)', f'{outFold}/WHF.tsv', f'{outFold}/WHF.{metric}.anova.tsv')
        anova(f'{metric} ~ C(MF, Sum) * C(Sel, Sum)', f'{outFold}/SO.tsv', f'{outFold}/SO.{metric}.anova.tsv')
        anova(f'{metric} ~ C(MF, Sum) * C(Sel, Sum) * C(DM, Sum)', f'{outFold}/MO.tsv', f'{outFold}/MO.{metric}.anova.tsv')


def processAnova(algs, outFold):
    data = [ ]
    for method in algs:
        values = { }
        for metric in Metricas:
            values[metric] = { }
            file = open(f'{outFold}/{method}.{metric}.anova.tsv', 'r')
            lines = file.readlines()
            file.close()
            factors = []
            for line in lines[2:-1]:
                line = line.strip().replace('C(', '').replace(', Sum)', '').split('\t')
                values[metric][line[0]] = 'Yes' if float(line[-1]) < 0.05 else 'N'
                factors.append(line[0])
        data.append({'Factor': method })
        for factor in factors:
            line = { 'Factor': f'{factor:10s}' }
            for metric in Metricas:
                line[metric] = f'{values[metric][factor]:10s}'
            data.append(line)
    data = pd.DataFrame(data, columns=['Factor']+Metricas)
    data.to_latex(f'{outFold}/anova.tex', col_space=10, index=False, na_rep='')


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    home = '/Users/reifortes/Documents/tese'
    bd = sys.argv[1]
    resultsHome = f'{home}/{bd}/{sys.argv[2]}'
    r1 = int(sys.argv[3])
    r2 = int(sys.argv[4])
    topN = int(sys.argv[5])
    doProcessFiles = sys.argv[6] in [ '1', 'True', 'Sim' ]
    doComputeAnova = sys.argv[7] in [ '1', 'True', 'Sim' ]
    outFold = f'{resultsHome}/{sys.argv[8]}'
    createPath(outFold)
    if doProcessFiles: processFiles(Algoritmos[bd], resultsHome, r1, r2, topN, outFold)
    if doComputeAnova: computeAnova(outFold)
    processAnova(Algoritmos[bd], outFold)
    print("Fim")

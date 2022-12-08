'''
Created on 07/04/2017
Updated on
@author: reifortes

Execution line: python3.4 ...
'''

import sys, os, glob

def convert(value):
    return float(value.replace(',', '.'))


def processConfigs(configsStr):
    configs = {}
    values = configsStr.split('/')
    for value in values:
        version = value.split(';')[0]
        configs[version] = value
    return configs


def processQualityIndicators(file):
    result = {}
    file = open(file, 'r')
    header = file.readline().strip().split(';')
    col = [header.index(x) for x in header if x == 'Hypervolume'][0]
    for line in file:
        line = line.strip().split(';')
        if '-seq_' in line[0]: continue
        version = line[0].split('_')[-1]
        alg = line[0].replace(f'_{version}', '')
        conf = ''
        if 'S-true' in alg:
            if   '_C-0.05' in alg: conf = '-0.05'
            elif '_C-0.1'  in alg: conf = '-0.1'
            alg = alg.replace(f'_C{conf}', f'_C')
        if alg not in result: result[alg] = {}
        result[alg][version+conf] = -1 * convert(line[col]) # invertendo - quanto maior melhor - a busca usa min
    return result


def processSOResults(path, result):
    files = glob.glob(f'{path}/*-FUN.tsv')
    for file in files:
        alg = os.path.basename(file)[:-11]
        version = os.path.basename(file)[-10:-8]
        file = open(file, 'r')
        line = file.readline().strip().split()
        if alg not in result: result[alg] = {}
        result[alg][version] = (convert(line[0]) + convert(line[1]) + convert(line[2])) / 3


def searchWinner(versions):
    winner = min(versions, key=versions.get) # quanto maior melhor, mas valores são negativados
    return winner


def getConfigLine(alg, home):
    if   alg.startswith('MO_'):      configFile = f'{home}/tuningMO.txt'
    elif alg.startswith('RISK_MO_'): configFile = f'{home}/tuningMORisk.txt'
    elif alg.startswith('FAIR_MO_'): configFile = f'{home}/tuningMOFair.txt'
    elif alg.startswith('SO_'):      configFile = f'{home}/tuningSO.txt'
    elif alg.startswith('RISK_SO_'): configFile = f'{home}/tuningSORisk.txt'
    elif alg.startswith('FAIR_SO_'): configFile = f'{home}/tuningSOFair.txt'
    file = open(configFile, 'r')
    lines = file.readlines()
    if 'SO' not in configFile: return lines[0]
    elif 'E-false' in alg: return lines[0]
    else: return lines[1]
    return None


def setMOAlgorithmParams(alg, newline, winner):
    params = alg.replace('RISK_', 'RISK-').replace('FAIR_', 'FAIR-').split('_')
    strategy = params[1]
    newline = newline.replace('<STRATEGY>', strategy)
    extreme = params[2].replace('E-', '')
    newline = newline.replace('<EXTREME>', extreme)
    stats = params[3].replace('S-', '')
    newline = newline.replace('<STATISTICALTEST>', stats)
    conf = '0'
    if  '-0.05' in winner: conf = '0.05'
    elif '-0.1' in winner: conf = '0.1'
    newline = newline.replace('<CONFIDENCE>', conf)
    if 'RISK_' in alg:
        alpha = params[5].replace('A-', '')
        newline = newline.replace('<ALPHA>', alpha)
    newline = newline.replace('MO/', 'MO/<FOLD>/')
    return newline


def setSOAlgorithmParams(alg, newline):
    params = alg.replace('RISK_', 'RISK-').replace('FAIR_', 'FAIR-').split('_')
    strategy = params[1]
    newline = newline.replace('<STRATEGY>', strategy)
    if 'RISK_' in alg:
        alpha = params[3].replace('A-', '')
        newline = newline.replace('<ALPHA>', alpha)
    newline = newline.replace('SO/', 'SO/<FOLD>/')
    return newline


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    home = sys.argv[1]
    qiFile = sys.argv[2]
    tuningConfigMO = processConfigs(sys.argv[3])
    pathSO = sys.argv[4]
    tuningConfigSO = processConfigs(sys.argv[5])
    outFile = f'{home}/{sys.argv[6]}'
    results = processQualityIndicators(qiFile)
    #Ini: Para não processar SO: comentar linha abaixo
    processSOResults(pathSO, results)
    #Fim: Para não processar SO
    outFile = open(outFile, 'w')
    for alg in results:
        winner = searchWinner(results[alg])
        print('- Version winner for %s: %s' % (alg, winner))
        configLine = getConfigLine(alg, home)
        #Ini: (artigo Fairness) para processar apenas RISK_SO (Amazon e ML20M) e FAIR_SO (todas as bases): descomentar linha abaixo
        if not ('RISK_SO' in alg or 'FAIR_SO' in alg): continue
        #Fim: (artigo Fairness) para processar apenas RISK_SO (Amazon e ML20M) e FAIR_SO (todas as bases)
        if 'MO_' in alg:
            #Ini: para processar apenas o que deu erro no ML20M: descomentar linhas abaixo
            #if ('MO_FWLS-sel_E-true_S-false_' not in alg) and ('MO_FWLS-sel_E-true_S-true_'  not in alg) and ('MO_HR-sel_E-true_S-true_' not in alg): continue
            #if ('RISK_' in alg): continue
            #Fim: para processar apenas o que deu erro no ML20M
            newline = configLine.replace('<MO_CONFIG>', tuningConfigMO[winner[0:2]])
            newline = setMOAlgorithmParams(alg, newline, winner)
        else:
            newline = configLine.replace('<SO_CONFIG>', tuningConfigSO[winner[0:2]])
            newline = setSOAlgorithmParams(alg, newline)
        outFile.write(newline)
        print(newline)
    outFile.close()
    print("Fim")

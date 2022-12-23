'''
Process the scikit tuning resulting files to be used in Scikit-Learn.

Created on 01/12/2015
Updated on 19/07/2017
Updated on 17/02/2019

@author: reifortes

Execution line: python3.4 ...
'''
import os, sys, gzip


algCreates = {
                'Ridge'    : 'Ridge(',
                'B-Ridge'  : 'BayesianRidge(',
                'Bag'      : 'BaggingRegressor(n_jobs=1, random_state=0, bootstrap=True, ',
                #'RFR'      : 'RandomForestRegressor(n_jobs=-1, random_state=0, bootstrap=True, ',
                'RFR'      : 'RandomForestRegressor(n_jobs=1, random_state=0, bootstrap=True, ',
                'AdaB'     : 'AdaBoostRegressor(random_state=0, ',
                'GBR'      : 'GradientBoostingRegressor(random_state=0, ',
                'LinearSVR': 'LinearSVR(random_state=0, ',
                'SVR'      : 'SVR(',
             }


def processFold(inPath, prefix, extension):
    print("processFold: %s" % (inPath))
    files = [ f for f in os.listdir(inPath) if (prefix in f and extension in f) ]
    for file in files:
        processFile(inPath, file)


def processFile(sourcePath, inFile):
    global configs
    print("processFile: %s" % (inFile))
    alg = ''
    path = ''
    file = ''
    if '.gz' in file: arqIn = gzip.open('%s%s' % (sourcePath, inFile), 'r')#, encoding="utf-8")
    else: arqIn = open('%s%s' % (sourcePath, inFile), 'r', encoding="utf-8")
    for line in arqIn:
        line = line.strip()
        if '- Algorithm: ' in line:
            alg = line.replace('- Algorithm: ', '')
        elif '- Path: ' in line:
            path = line.replace('- Path: ', '')
        elif '- File: ' in line:
            file = line.replace('- File: ', '')
        elif '- Best score: ' in line:
            score = float(line.replace('- Best score: ', ''))
        elif '- Parameters: ' in line:
            if path not in configs: configs[path] = {}
            if file not in configs[path]:
                configs[path][file] = [ score, alg, line.replace('- Parameters: ', '').replace('\': ', '=').replace(', \'', ', ').replace('{\'', '').replace('}', '') ]
            elif configs[path][file][0] < score:
                configs[path][file] = [ score, alg, line.replace('- Parameters: ', '').replace('\': ', '=').replace(', \'', ', ').replace('{\'', '').replace('}', '') ]

    arqIn.close()


def saveAlgorithms(outPut):
    global configs
    outPutFile = open(outPut, 'w', encoding="utf-8")
    outPutFile.write('from sklearn.datasets import load_svmlight_file\n')
    outPutFile.write('from sklearn.linear_model import Ridge\n')
    outPutFile.write('from sklearn.linear_model import BayesianRidge\n')
    outPutFile.write('from sklearn.linear_model import SGDRegressor\n')
    outPutFile.write('from sklearn.isotonic import IsotonicRegression\n')
    outPutFile.write('from sklearn.ensemble import BaggingRegressor\n')
    outPutFile.write('from sklearn.ensemble import RandomForestRegressor\n')
    outPutFile.write('from sklearn.ensemble import AdaBoostRegressor\n')
    outPutFile.write('from sklearn.ensemble import GradientBoostingRegressor\n')
    outPutFile.write('from sklearn.svm import LinearSVR\n')
    outPutFile.write('from sklearn.svm import SVR\n\n')
    outPutFile.write('algorithms = {\n')
    TabsPath = '\t' * 1
    TabsFile = '\t' * 2
    paths = sorted(configs.keys())
    for path in paths:
        outPutFile.write('%s\'%s\': {\n' % (TabsPath, path))
        files = sorted(configs[path].keys())
        for file in files:
            alg = configs[path][file][1]
            outPutFile.write('%s\'%s\': %s%s),\n' % (TabsFile, file, algCreates[alg], configs[path][file][2]))
        outPutFile.write('%s}\n' % TabsFile)
    outPutFile.write('}\n')
    outPutFile.close()


if __name__ == '__main__':
    print("Inicio")
    home      = sys.argv[1]#'/Users/reifortes/Downloads/temp/Execution05/ML-100K/Scikit-Norm/Tuning/'
    prefix    = sys.argv[2]#'scikitTuning-'
    extension = sys.argv[3]#'.out'
    outPut    = sys.argv[4]#'/Users/reifortes/Downloads/temp/Execution05/ML-100K/Scikit-Norm/scikitAlgorithms.py'
    configs  = {}
    processFold(home, prefix, extension)
    saveAlgorithms(outPut)
    print("Fim")

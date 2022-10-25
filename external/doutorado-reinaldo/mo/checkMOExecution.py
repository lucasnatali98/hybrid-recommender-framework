# -*- coding: utf-8 -*-
'''
Avaliar os resultados de metodos MO com relação às quantidades de soluções
Created on 19/11/2019
Updated on
@author: reifortes
'''

import sys
sys.path.insert(0, '/Users/reifortes/Downloads/temp/execution11/run/')
sys.path.insert(0, '/home/terralab/reinaldo/execution11/run')

import util


def setConfigQtd(line, results, key):
    config = line.split('(')[1].split(')')[0]
    value = int(line.split('): ')[1].split(' ')[0].replace('ms', ''))
    if config not in results: results[config] = {}
    results[config][key] = value


def getOutString(config, results):
    line =  "'%s" % config[:2]
    configName = config[3:]
    configName = ('%s_All' % configName.split('-')[0]) if '-all-' in configName else ('%s_FS' % configName.split('_')[0])
    line += '\t%s' % configName
    line += '\t%s' % ('true' if 'D_true' in config else 'false')
    line += '\t%s' % ('true' if 'S_true' in config else 'false')
    line += '\t%s' % (config.split('_C_')[1])
    line += '\t%d' % results[config]['Solutions']
    line += '\t%d' % results[config]['Population']
    line += '\t%d' % results[config]['Pareto']
    return line


def processExecMOout(inFileName, outFileName):
    results = {}
    inFile = open(inFileName, 'r')
    for line in inFile:
        line = line.strip()
        if 'JMetal solutions created' in line:
            setConfigQtd(line, results, 'Solutions')
        elif 'Total execution time' in line:
            setConfigQtd(line, results, 'Time')
    inFile.close()
    outFile = open(outFileName, 'w')
    outFile.write('ConfigName\tSolutions\tTime\n')
    for config in results:
        outFile.write(f'{config}\t{results[config]["Solutions"]}\t{results[config]["Time"]}\n')
    outFile.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    util.using("Inicio")
    homeDir = sys.argv[1] #/Users/reifortes/Downloads/temp/execution11/Bookcrossing/out
    inExecMOoutFile = '%s/%s.out' % (homeDir, sys.argv[2]) # execMO-1-1-New
    outExecMOoutFile = inExecMOoutFile.replace('.out', '.tsv')
    processExecMOout(inExecMOoutFile, outExecMOoutFile)
    util.using("Fim")
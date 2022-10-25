'''
Created on 07/04/2017
Updated on
@author: reifortes

Execution line: python3.4 ...
'''

import os, sys, glob, subprocess, shutil
from util import getAlgName
from util import createPath


def getQtds(file):
    inFile = open(file, 'r')
    lines = inFile.readlines()
    inFile.close()
    qtdSol = len(lines)
    return qtdSol


def processFiles(set, files, outFold, command):
    print(f'- Processing {set}')
    for file in files:
        alg = getAlgName(os.path.basename(file))
        print(f'. Alg: {alg}')
        outFile = f'{outFold}/{alg}.tsv'
        if os.path.exists(outFile):
            outFile = open(outFile, 'a')
        else:
            outFile = open(outFile, 'w')
            outFile.write('Set\tSeq\tHypervolume\tQtdSolutions\n')
        if '-seq_' in file:
            seq = int(file.split('-seq_')[1].split('-')[0])
        else:
            seq = -1
        result = subprocess.Popen([command, '-r 0 0 0', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = result.communicate()
        qtdSol = getQtds(file)
        outFile.write(f'{set}\t{seq}\t{out.decode("utf-8").strip()}\t{qtdSol}\n')
        outFile.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    command = sys.argv[1]
    bd = sys.argv[2]
    moHome = f'{bd}/{sys.argv[3]}'
    outFold = f'{bd}/{sys.argv[4]}'
    #shutil.rmtree(outFold, ignore_errors=True)
    createPath(outFold)
    files = glob.glob(f'{moHome}/*-FUN.tsv')
    popFiles = [ f for f in files if '-PF-' not in f ]
    pfFiles = [ f for f in files if '-PF-' in f ]
    processFiles('Pop', popFiles, outFold, command)
    processFiles('PF', pfFiles, outFold, command)
    print("Fim")

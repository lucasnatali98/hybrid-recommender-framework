'''
Created on 07/04/2017
Updated on
@author: reifortes

Execution line: python3.4 ...
'''

import os, sys, glob
import subprocess


if __name__ == '__main__':
    print("Inicio")
    command = sys.argv[1]
    home = sys.argv[2]
    fold = sys.argv[3]
    outFile = '%s%s' % (home, sys.argv[4])
    outFile = open(outFile, 'w')
    outFile.write('Solution;Hypervolume;\n')
    files = glob.glob('%s%s/*-PF-FUN.tsv' % (home, fold))
    for file in files:
        result = subprocess.Popen([command, '-r 0 0 0', file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = result.communicate()
        outFile.write('%s;%s;\n' % (os.path.basename(file).replace('-PF-FUN.tsv', ''), out.decode('utf-8').strip()))
    outFile.close()
    print("Fim")

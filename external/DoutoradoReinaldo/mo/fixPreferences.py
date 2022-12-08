'''
Criar arquivo de preferências para os usuários de tuning.
'''

import sys, os, random
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


def readUsers(fileName):
    users = set()
    file = open(fileName, 'r')
    for line in file:
        line = line.strip().split()
        uid = int(line[0])
        users.add(uid)
    file.close()
    return users


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    folds = [ 1, 2, 3, 4, 5 ]
    for fold in folds:
        users = readUsers(f'{home}/BD/Sample{fold}.test')
        fileName = f'{home}/BD/Sample{fold}.preferences'
        os.rename(fileName, fileName+'.old')
        inFile = open(fileName+'.old', 'r')
        outFile = open(fileName, 'w')
        for line in inFile:
            uid = int(line.strip().split()[0])
            users.remove(uid)
            if 'nan' in line: line = f'{uid}\t{1/3:.6f}\t{1/3:.6f}\t{1/3:.6f}\n'
            outFile.write(line)
        for uid in users:
            outFile.write(f'{uid}\t{1/3:.6f}\t{1/3:.6f}\t{1/3:.6f}\n')
    outFile.close()
    util.using("Fim")

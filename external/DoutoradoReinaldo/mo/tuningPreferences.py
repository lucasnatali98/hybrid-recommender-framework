'''
Criar arquivo de preferências para os usuários de tuning.
'''

import sys, os, random
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


def readUsers(home):
    users = {}
    file = open(f'{home}/BD/tuning.users', 'r')
    for line in file:
        line = line.strip().split()
        fold = int(line[0])
        uid = int(line[1])
        if fold not in users: users[fold] = set()
        users[fold].add(uid)
    file.close()
    return users


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    users = readUsers(home)
    outFile = open(f'{home}/BD/tuning.preferences', 'w')
    folds = [ 1, 2, 3, 4, 5 ]
    for fold in folds:
        inFile = open(f'{home}/BD/Sample{fold}.preferences', 'r')
        for line in inFile:
            uid = int(line.strip().split()[0])
            if uid in users[fold]:
                if 'nan' in line: line = f'{uid}\t{1/3:.6f}\t{1/3:.6f}\t{1/3:.6f}\n'
                outFile.write(line)
    outFile.close()
    util.using("Fim")

'''
Selecionar dados para tuning dos métodos híbridos.
Seleciona um % de usuários diferentes de cada fold.
'''

import sys, os, random
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


def selectUsers(home, folds, percent):
    users = set()
    outFile = open(f'{home}/BD/tuning.users', 'w')
    for fold in folds:
        file = open(f'{home}/BD/Sample{fold}.test', 'r')
        foldUsers = set()
        for line in file:
            line = line.strip().replace('.0', '').split()
            uid = int(line[0])
            foldUsers.add(uid)
        qtd = int(len(foldUsers) * percent)
        foldUsers = foldUsers.difference(users)
        selected = random.sample(foldUsers, qtd)
        users = users.union(selected)
        for user in selected:
            outFile.write(f'{fold}\t{user}\n')
    outFile.close()
    return users


def getFoldName(fold):
    return f'F{"12345".replace(str(fold), "")}-{fold}'


def writeFiles(featuresHome, outputHome, folds, users):
    outKeysFile = open(f'{outputHome}/keys.train', 'w')
    outHrAllFile = open(f'{outputHome}/HR-all.train', 'w')
    outStreamAllFile = open(f'{outputHome}/STREAM-all.train', 'w')
    outFwlsAllFile = open(f'{outputHome}/FWLS-all.train', 'w')
    outHrSelFile = open(f'{outputHome}/HR-sel.train', 'w')
    outStreamSelFile = open(f'{outputHome}/STREAM-sel.train', 'w')
    outFwlsSelFile = open(f'{outputHome}/FWLS-sel.train', 'w')
    for fold in folds:
        inKeysFile = open(f'{featuresHome}/{getFoldName(fold)}/keys.train', 'r')
        inHrAllFile = open(f'{featuresHome}/{getFoldName(fold)}/HR-all.train', 'r')
        inStreamAllFile = open(f'{featuresHome}/{getFoldName(fold)}/STREAM-all.train', 'r')
        inFwlsAllFile = open(f'{featuresHome}/{getFoldName(fold)}/FWLS-all.train', 'r')
        inHrSelFile = open(f'{featuresHome}/{getFoldName(fold)}/HR-sel.train', 'r')
        inStreamSelFile = open(f'{featuresHome}/{getFoldName(fold)}/STREAM-sel.train', 'r')
        inFwlsSelFile = open(f'{featuresHome}/{getFoldName(fold)}/FWLS-sel.train', 'r')
        for keys, hrAll, streamAll, fwlsAll, hrSel, streamSel, fwlsSel in zip(inKeysFile, inHrAllFile, inStreamAllFile, inFwlsAllFile, inHrSelFile, inStreamSelFile, inFwlsSelFile):
            uid = int(keys.strip().split(',')[0])
            if uid in users:
                outKeysFile.write(keys)
                outHrAllFile.write(hrAll)
                outStreamAllFile.write(streamAll)
                outFwlsAllFile.write(fwlsAll)
                outHrSelFile.write(hrSel)
                outStreamSelFile.write(streamSel)
                outFwlsSelFile.write(fwlsSel)
    outKeysFile.close()
    outHrAllFile.close()
    outStreamAllFile.close()
    outFwlsAllFile.close()
    outHrSelFile.close()
    outStreamSelFile.close()
    outFwlsSelFile.close()


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    featuresHome = f'{home}/{sys.argv[2]}'
    percent = float(sys.argv[3])
    outputHome = f'{featuresHome}/{sys.argv[4]}'
    if not os.path.exists(outputHome): os.makedirs(outputHome)
    folds = [ 1, 2, 3, 4, 5 ]
    users = selectUsers(home, folds, percent)
    writeFiles(featuresHome, outputHome, folds, users)
    util.using("Fim")

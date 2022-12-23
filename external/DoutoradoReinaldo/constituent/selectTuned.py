import sys, os, glob
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


def processEvalTxt(home, winnersFile):
    algoritms = [ 'ALS_BiasedMF', 'Bias.', 'BiasedSVD', 'ImplicitMF', 'ItemKNN', 'TF_BiasedMF', 'UserKNN', 'cbpr', 'ncf' ]
    for nameAlg in algoritms:
        versions = {}
        files = glob.glob(f'{home}/constituent/F???-?/{nameAlg}*eval.txt')
        for file in files:
            version = os.path.basename(file).replace('.eval.txt', '')
            file = open(file, 'r')
            value = None
            for eval in file:
                eval = eval.strip().split()
                if eval[0] == 'rmse': value = float(eval[1])
            if value:
                if version not in versions: versions[version] = 0
                versions[version] += value
        if len(versions) > 0:
            for version in versions: versions[version] /= len(versions)
            winner = min(versions, key=versions.get)
            winnersFile.write(f'{winner}\t{versions[winner]}\n')


def processMyMediaLite(home, winnersFile):
    logPath = f'{home}/out/constituent'
    algoritms = [ 'BiasedMatrixFactorization', 'BiPolarSlopeOne', 'SlopeOne', 'SVDPlusPlus' ]
    for nameAlg in algoritms:
        versions = {}
        files = glob.glob(f'{logPath}/2_myMediaLiteTuning_???-?_{nameAlg}*-F???-?.out')
        for file in files:
            version = nameAlg + os.path.basename(file).split(nameAlg)[-1].split('-F')[0]
            file = open(file, 'r')
            allLines = file.readlines()
            value = None
            for l in range(len(allLines)-1, -1, -1):
                if ' RMSE ' in allLines[l]:
                    values = allLines[l].strip().split(' RMSE ')
                    value = float(values[-1].split(' ')[0].replace(',', '.'))
                    break
            if value:
                if version not in versions: versions[version] = 0
                versions[version] += value
        if len(versions) > 0:
            for version in versions: versions[version] /= len(versions)
            winner = min(versions, key=versions.get)
            winnersFile.write(f'{winner}\t{versions[winner]}\n')


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    outFold = sys.argv[2]
    winnersFile = open(f'{outFold}/{sys.argv[3]}.txt', 'w')
    processEvalTxt(home, winnersFile)
    processMyMediaLite(home, winnersFile)
    winnersFile.close()
    util.using("Fim")

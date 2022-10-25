import sys
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


def readWinners(winnersFile):
    file = open(winnersFile, 'r')
    winners = set()
    for line in file:
        line = line.strip().split()
        name = line[0]
        # tratando nomes que ocorrem em outros algoritmos
        if   name == 'Bias'    : name = ' Bias '
        elif name == 'SlopeOne': name = '/SlopeOne.'
        winners.add(name)
    return winners


def processFile(fileName, winners, outFile):
    executionFile = open(fileName, 'r')
    for line in executionFile:
        for winner in winners:
            if winner in line:
                outFile.write(line.replace("#", "").replace('<TEST1><TEST2>', '<TEST>').replace('<TEST1>', '<TEST>').replace('<TEST2>', '""'))
                break


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    winnersFile = f'run/constituent/{sys.argv[2]}'
    outFile = open(f'run/constituent/{sys.argv[3]}', 'w')
    winners = readWinners(winnersFile)
    processFile(f'run/constituent/{sys.argv[4]}Tuning.txt', winners, outFile)
    #processFile('run/constituent/lensKitTuning.txt', winners, outFile)
    #processFile('run/constituent/myMediaLiteTuning.txt', winners, outFile)
    #processFile('run/constituent/ncfTuning.txt', winners, outFile)
    #processFile('run/constituent/cbprTuning.txt', winners, outFile)
    outFile.close()
    util.using("Fim")
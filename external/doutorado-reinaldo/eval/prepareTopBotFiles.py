import sys, os, glob, time, random


def readUsers(weightsFile):
    # Seleção dos Usuários:
    #  - ALL
    #  - TOP: 1 / 5 dos primeiros (ordenação por acurácia) = Accuracy Tolerant
    #  - BOT: 1 / 5 dos últimos (ordenação por acurácia)   = High Accuracy
    users = {}
    file = open(weightsFile, 'r')
    lines = file.readlines()
    file.close()
    qtdALL = len(lines)
    qtdPart = int(qtdALL * 0.2) # 20% dos usuários
    #qtdPart = int(qtdALL * 0.1) # 10% dos usuários
    for l in range(qtdALL):
        line = lines[l].strip().split()
        id = int(line[0])
        # cada elemento é: chave = id, valor = (TOP, BOT)
        users[id] = (l < qtdPart, l >= qtdALL-qtdPart)
    return users

def processFile(users, inName, topName, botName):
    inFile = open(inName, 'r')
    topFile = open(topName, 'w')
    botFile = open(botName, 'w')
    for line in inFile:
        id = int(line.split()[0])
        if id in users:
            if users[id][0]: topFile.write(line)
            if users[id][1]: botFile.write(line)
    inFile.close()
    topFile.close()
    botFile.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    dataset = sys.argv[1]
    predHomes = sys.argv[2].split(';')
    weightsFile = f'{dataset}/{sys.argv[3]}'
    r1 = int(sys.argv[4])
    r2 = int(sys.argv[5])
    fold = sys.argv[6]
    users = readUsers(weightsFile)
    # test files
    filePrefix = f'{dataset}/BD/Sample{fold.split("-")[1]}'
    processFile(users, f'{filePrefix}.test', f'{filePrefix}.top.test', f'{filePrefix}.bot.test')
    # prediction files
    for predHome in predHomes:
        predHome = f'{dataset}/{predHome}'
        for r in range(r1, r2+1):
            inPath = f'{predHome}/R{r}/{fold}'
            topPath = f'{predHome}/R{r}-Top/{fold}'
            time.sleep(random.randint(0, 5))
            if not os.path.exists(topPath): os.makedirs(topPath)
            botPath = f'{predHome}/R{r}-Bot/{fold}'
            time.sleep(random.randint(0, 5))
            if not os.path.exists(botPath): os.makedirs(botPath)
            files = glob.glob(f'{inPath}/*.sorted')
            for file in files:
                baseName = os.path.basename(file)
                processFile(users, file, f'{topPath}/{baseName}', f'{botPath}/{baseName}')
    print("Fim")

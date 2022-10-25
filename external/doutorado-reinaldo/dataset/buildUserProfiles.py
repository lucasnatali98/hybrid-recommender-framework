'''
Cria o perfil do usuário de acordo com os itens relevantes
'''
import sys, csv
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


def readContent(fileName):
    file = open(fileName, 'r')
    content = {}
    for row in file:
        row = row.strip().split('|')
        iid = int(row[0])
        content[iid] = row[1]
    file.close()
    return content


def readRelevantItens(fileName, cutoff):
    file = open(fileName, 'r')
    ratings = csv.reader(file, delimiter='\t')
    userRel = {}
    for row in ratings:
        uid = int(row[0])
        iid = int(row[1])
        value = float(row[2])
        if value >= cutoff:
            if uid not in userRel: userRel[uid] = []
            userRel[uid].append(iid)
    file.close()
    return userRel


def buildProfile(relevantItems, content):
    profile = ''
    for iid in relevantItems:
        if iid in content: profile += ' ' + content[iid]
    return profile


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    contentFile = f'{home}/BD/{sys.argv[2]}'
    folds = sys.argv[3].split(';')
    cutoff = float(sys.argv[4])
    content = readContent(contentFile)
    for f in folds:
        userRelevantItens = readRelevantItens(f'{home}/BD/Sample{f}.train', cutoff)
        outFile = open(f'{home}/BD/Sample{f}.user.profile', 'w')
        for uid in userRelevantItens:
            profile = buildProfile(userRelevantItens[uid], content)
            outFile.write(f'{uid}|{profile}\n')
        outFile.close()
    util.using("Fim")

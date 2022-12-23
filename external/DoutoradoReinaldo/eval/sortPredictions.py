'''
Prepare predictions to be used in RankSys evaluation.

Created on 08/08/2015
Updated on 02/04/2017 Location of the prediction fold
@author: reifortes

Execution line: python3.4 evaluationMetrics.py a b Predictions/ BD/ML-100k/forPred- 'Fold1' 'UserItemBaseline' c

python3.4 evaluationMetrics.py ...

reifortes$
'''

import sys, operator, glob


class Prediction:
    user = None
    item = None
    value = None
    def __init__(self, userId, itemId, value):
        self.user = userId
        self.item = itemId
        self.value = value
    def getStr(self):
        return f'{self.user}\t{self.item}\t{self.value}\n'


# alguns usuários saíram do teste
def readUsers(file):
    users = []
    infile = open(file, 'r')
    for line in infile:
        line = line.strip().split(',')
        uid = int(line[0])
        if uid not in users: users.append(uid)
    infile.close()
    return users


def processFile(fileName, users, topn):
    print('- File: %s' % filename)
    predictions = readPredictionsFile(fileName, users)
    out = open(fileName+'.sorted', 'w')
    for user in sorted(predictions):
        predictions[user].sort(key=operator.attrgetter("value"), reverse=True)
        for i in range(min(topn, len(predictions[user]))):
            out.write(predictions[user][i].getStr())
    out.close()


def readPredictionsFile(fileName, users):
    arq = open(fileName, 'r')
    predictions = {}
    for line in arq:
        if 'nan' in line: continue # inserido após execução da avaliação, pois foi identificado erro devido à ocorrência de nan nas predições MO
        values = line.strip().replace(',', '\t').split()
        if len(values) < 3: continue
        (userId, itemId, value) = values[:3]
        if not userId.isdigit(): continue
        userId = int(userId)
        if userId not in users: continue
        itemId = int(itemId)
        value = float(value)
        prediction = Prediction(userId, itemId, value)
        if userId not in predictions: predictions[userId] = []
        predictions[userId].append(prediction)
    arq.close()
    return predictions


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    dataSet        = sys.argv[1]
    predictionPath = f'{dataSet}/{sys.argv[2]}'
    users = readUsers(f'{dataSet}/{sys.argv[3]}')
    topn = int(sys.argv[4])
    if topn <= 0: topn = float('inf')
    files = glob.glob(f'{predictionPath}/*.tsv')
    for filename in files:
        processFile(filename, users, topn)
    print("Término")

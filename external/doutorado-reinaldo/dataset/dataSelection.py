'''
Select 5-fold crossvalidation with Probe, Test and Training partitions.

The selection is proportional of the number of ratings by users.
'''
import os,sys,csv
import math
from random import shuffle
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util

class Rating:
    user = None
    item = None
    rating = None
    dateTime = None
    def __init__(self, userId, itemId, rating, dateTime):
        self.user = userId
        self.item = itemId
        self.rating = rating
        self.dateTime = dateTime


def readRatingsFile(fileName):
    print("readRatingsFile: %s" % fileName)
    data = {}
    file = open(fileName, 'r')
    ratings = csv.reader(file, delimiter='\t')
    for row in ratings:
        uid = int(row[0])
        iid = int(row[1])
        value = float(row[2])
        dt = int(row[3])
        r = Rating(uid, iid, value, dt)
        if uid not in data: data[uid] = []
        data[uid].append(r)
    file.close()
    return data


def selectFolds(ratings, numFolds):
    print("selectFolds")
    F = []
    for n in range(0, numFolds): F.append([])
    print(" - Number of users: " + str(len(ratings)))
    count = 0
    over = 0
    for uid in ratings:
        userRatings = ratings[uid]
        if len(userRatings) <= 10: continue
        shuffle(userRatings)
        qtd = math.floor(len(userRatings) / numFolds)
        start = 0
        finish = qtd
        for n in range(0, numFolds):
            F[n] += userRatings[start:finish]
            start += qtd
            finish += qtd
        for r in userRatings[start:]:
            F[over%numFolds].append(r)
            over += 1
        count += 1
    print(" - " + str(count) + " users processsed.")
    return F


def getTest(foldData):
    countRatings = {}
    for r in foldData:
        if r.user not in countRatings: countRatings[r.user] = 0
        countRatings[r.user] += 1
    print(f'  - Train users: {len(countRatings)}')
    data = []
    countUsers = set()
    for r in foldData:
        if countRatings[r.user] >= cutoff:
            data.append(r)
            countUsers.add(r.user)
    print(f'  - Test users: {len(countUsers)}')
    return data


def saveFile(fileName, ratings):
    file = open(fileName, 'w')
    ratingsNorm = csv.writer(file, delimiter='\t')
    for r in ratings:
        ratingsNorm.writerow([r.user, r.item, r.rating, r.dateTime])
    file.close()


def saveFiles(F, outPutFolder):
    print("saveFiles:")
    numFolds = len(F)
    for n in range(0, numFolds):
        fileName = f'{outPutFolder}/Sample{n+1}'
        print(f" - {fileName}:")
        saveFile(f'{fileName}.train', F[n])
        saveFile(f'{fileName}.test', getTest(F[n]))
    # Saving combined files
    combinations = [    [1, 2, 3],
                        [1, 2, 4],
                        [1, 2, 5],
                        [1, 3, 4],
                        [1, 3, 5],
                        [1, 4, 5],
                        [2, 3, 4],
                        [2, 3, 5],
                        [2, 4, 5],
                        [3, 4, 5],
                        [1, 2, 3, 4],
                        [1, 2, 3, 5],
                        [1, 2, 4, 5],
                        [1, 3, 4, 5],
                        [2, 3, 4, 5]
                   ]
    for c in range(0, len(combinations)):
        commandLine = 'cat '
        rFile = f'{outPutFolder}/Sample'
        for n in combinations[c]:
            commandLine += f'{outPutFolder}/Sample{n}.train '
            rFile += f'{n}'
        rFile += '.train'
        commandLine += f'> {rFile}'
        print(commandLine)
        os.system(commandLine)


if __name__ == '__main__':
    util.using("Inicio")
    home = sys.argv[1]
    ratingFile = f'{home}/BD/{sys.argv[2]}'
    outPutFolder = f'{home}/BD'
    numFolds = int(sys.argv[3])
    cutoff = int(sys.argv[4])
    ratings = readRatingsFile(ratingFile)
    F = selectFolds(ratings, numFolds)
    for n in range(0, numFolds):
        print(' - Fold %d (%d)' % (n+1, len(F[n])))
    saveFiles(F, outPutFolder)
    util.using("Fim")

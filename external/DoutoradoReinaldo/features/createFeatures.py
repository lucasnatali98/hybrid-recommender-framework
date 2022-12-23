import sys, os, glob, csv
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


def readUsers(testFile):
    users = set()
    file = open(testFile, 'r')
    for line in file:
        line = line.strip().replace('.0', '').split()
        uid = int(line[0])
        users.add(uid)
    return users


def readRatings(fileName, users):
    ratings = {}
    reader = csv.reader(open(fileName, 'r'), delimiter='\t')
    for row in reader:
        uid = int(row[0])
        if uid not in users: continue
        ratings[f'{row[0]},{row[1]}'] = float(row[2])
    return ratings


def readPrediction(fold, features, users, pred):
    for fKey in range(1, len(features) + 1):
        feature = features[fKey - 1]
        file = open(f'{fold}/{feature}.tsv', 'r')
        for line in file:
            line = line.strip().split() if feature != 'CB_Lucene' else line.strip().split(',')
            try:
                user = int(line[0].replace('.0', ''))
                if user not in users: continue
                item = int(line[1].replace('.0', ''))
                value = float(line[2])
            except:
                continue
            uiKey = f'{user},{item}'
            if uiKey not in pred: pred[uiKey] = {}
            pred[uiKey][fKey] = value
        file.close()


def readNoFoldMetadata(home, metadatas):
    metaValues = {}
    for fKey in range(1, len(metadatas)+1):
        metadata = metadatas[fKey-1] # conferir indices / chaves
        fileName = f'{home}/Metadata/{metadata}.txt'
        if not os.path.exists(fileName): continue
        metaValues[fKey] = {}
        file = open(fileName, 'r')
        for line in file:
            line = line.strip().split(';')
            try:
                id = int(line[0])
                value = float(line[1])
            except:
                continue
            metaValues[fKey][id] = value
        file.close()
    return metaValues


def readMetadata(home, fold, features, noFoldMeta):
    meta = {}
    for fKey in range(1, len(features) + 1):
        feature = features[fKey-1]
        if os.path.exists(f'{home}/Metadata/{feature}.txt'):
            meta[fKey] = noFoldMeta[fKey]
            continue
        file = open(f'{home}/Metadata/{fold}/{feature}.txt', 'r')
        for line in file:
            line = line.strip().split(';')
            try:
                id = int(line[0])
                value = float(line[1])
            except:
                continue
            if fKey not in meta: meta[fKey] = {}
            meta[fKey][id] = value
        file.close()
    return meta


def processHRTrain(home, outFold, train, features, users):
    global ignoreCB
    predTrain = {}
    keysFolds = []
    sklTrain = open(f'{outFold}/HR-all.train', 'w')
    keysFile = open(f'{outFold}/keys.train', 'w')
    for tempTest in train:
        tempTrain = train.replace(tempTest, '')
        readPrediction(f'{home}/constituent/F{tempTrain}-{tempTest}', features, users, predTrain)
        ratings = readRatings(f'{home}/BD/Sample{tempTest}.test', users)
        keys = sorted(ratings)
        for uiKey in keys:
            keysFile.write(f'{uiKey}\n')
            keysFolds.append(f'F{tempTrain}-{tempTest}')
            sklTrain.write(f'{ratings[uiKey]:.10f}')
            for fKey in range(1, len(features)+1):
                sklTrain.write(f' {fKey}:{predTrain[uiKey][fKey] if fKey in predTrain[uiKey] else 0:.10f}')
            sklTrain.write('\n')
    sklTrain.close()
    keysFile.close()
    return keysFolds


def processHRTest(home, outFold, train, test, features, users):
    predTest = {}
    readPrediction(f'{home}/constituent/F{train}-{test}', features, users, predTest)
    # writing files
    ratings = readRatings(f'{home}/BD/Sample{test}.test', users)
    sklTest = open(f'{outFold}/HR-all.test', 'w')
    keysFile = open(f'{outFold}/keys.test', 'w')
    testKeys = sorted(ratings)
    for uiKey in testKeys:
        keysFile.write(f'{uiKey}\n')
        sklTest.write(f'{ratings[uiKey]:.10f}')
        for fKey in range(1, len(features) + 1):
            sklTest.write(f' {fKey}:{predTest[uiKey][fKey] if fKey in predTest[uiKey] else 0:.10f}')
        sklTest.write('\n')
    sklTest.close()
    keysFile.close()


def createHRFeatures(home, train, test, outFold):
    global ignoreCB
    users = readUsers(f'{home}/BD/Sample{test}.test')
    # features
    features = []
    featuresFile = open(f'{outFold}/HR-all.features', 'w')
    files = glob.glob(f'{home}/constituent/F{train}-{test}/*.tsv')
    for file in sorted(files):
        algName = os.path.basename(file).replace('.tsv', '')
        if ignoreCB and algName == 'CB_Lucene': continue
        features.append(algName)
        featuresFile.write(f'{len(features)}: {algName}\n')
    featuresFile.close()
    # train data
    keysFolds = processHRTrain(home, outFold, train, features, users )
    # test data
    processHRTest(home, outFold, train, test, features, users)
    return [features, keysFolds]


def processSTREAMTrain(home, outFold, constituents, metadatas, keysFolds):
    streamSklFile = open(f'{outFold}/STREAM-all.train', 'w')
    hrFile = open(f'{outFold}/HR-all.train', 'r')
    keysFile = open(f'{outFold}/keys.train', 'r')
    fold = None
    noFoldMetadata = readNoFoldMetadata(home, metadatas)
    for keys, line, keyFold in zip(keysFile, hrFile, keysFolds):
        keys = keys.strip().split(',')
        line = line.strip()
        if fold != keyFold:
            fold = keyFold
            mfValues = readMetadata(home, fold, metadatas, noFoldMetadata)
        streamSklFile.write(f'{line}')  # constituents HR
        qtdConst = len(constituents)
        for metadataKey in range(1, len(metadatas)+1):
            metadata = metadatas[metadataKey-1]
            keyIndex = 0 if metadata.endswith('_User') else 1
            id = int(keys[keyIndex])
            mfValue = mfValues[metadataKey][id] if id in mfValues[metadataKey] else 0
            streamSklFile.write(f' {qtdConst+metadataKey}:{mfValue:.10f}')
        streamSklFile.write('\n')
    hrFile.close()
    keysFile.close()
    streamSklFile.close()


def processSTREAMTest(home, outFold, train, test, constituents, metadatas):
    streamSklFile = open(f'{outFold}/STREAM-all.test', 'w')
    hrFile = open(f'{outFold}/HR-all.test', 'r')
    keysFile = open(f'{outFold}/keys.test', 'r')
    noFoldMetadata = readNoFoldMetadata(home, metadatas)
    mfValues = readMetadata(home, f'F{train}-{test}', metadatas, noFoldMetadata)
    for keys, line in zip(keysFile, hrFile):
        keys = keys.strip().split(',')
        line = line.strip()
        streamSklFile.write(f'{line}')  # constituents HR
        qtdConst = len(constituents)
        for metadataKey in range(1, len(metadatas)+1):
            metadata = metadatas[metadataKey-1]
            keyIndex = 0 if metadata.endswith('_User') else 1
            id = int(keys[keyIndex])
            mfValue = mfValues[metadataKey][id] if id in mfValues[metadataKey] else 0
            streamSklFile.write(f' {qtdConst+metadataKey}:{mfValue:.10f}')
        streamSklFile.write('\n')
    hrFile.close()
    keysFile.close()
    streamSklFile.close()


def createSTREAMFeatures(home, train, test, outFold, constituents, keysFolds):
    global ignoreCB
    # features
    featuresFile = open(f'{outFold}/STREAM-all.features', 'w')
    for key in range(0, len(constituents)):
        featuresFile.write(f'{key+1}: {constituents[key]}\n')
    files = glob.glob(f'{home}/Metadata/*.txt')
    files.extend(glob.glob(f'{home}/Metadata/F{train}-{test}/*.txt'))
    metadatas = []
    for file in sorted(files):
        metadataName = os.path.basename(file).replace('.txt', '')
        if ignoreCB and metadataName.startswith('cb_'): continue
        metadatas.append(metadataName)
        featuresFile.write(f'{len(constituents) + len(metadatas)}: {metadataName}\n')
    featuresFile.close()
    # train data
    processSTREAMTrain(home, outFold, constituents, metadatas, keysFolds)
    # test data
    processSTREAMTest(home, outFold, train, test, constituents, metadatas)
    return metadatas


def createFWLSFeatures(outputFolder, constituents, metadatas, ext, createFeaturesFile):
    if createFeaturesFile:
        fwlsFeaturesFile = open(f'{outputFolder}/FWLS-all.features', 'w')
        for fKey in range(0, len(constituents)):
            fwlsFeaturesFile.write(f'{fKey+1}: {constituents[fKey]}\n')
        fKey = len(constituents) + 1
        for mKey in range(0, len(metadatas)):
            fwlsFeaturesFile.write(f'{fKey}: {metadatas[mKey]}\n')
            fKey += 1
        fFwlsKey = fKey
        for meta in metadatas:
            for const in constituents:
                fwlsFeaturesFile.write(f'{fFwlsKey}: {meta}_*_{const}\n')
                fFwlsKey += 1
        fwlsFeaturesFile.close()
    fwlsSklFile = open(f'{outputFolder}/FWLS-all.{ext}', 'w')
    streamFile = open(f'{outputFolder}/STREAM-all.{ext}', 'r')
    for line in streamFile:
        line = line.strip()
        fwlsSklFile.write(f'{line}')
        line = line.split(' ')
        constValues = [ float(x.split(':')[1]) for x in line[1:len(constituents)+1] ]
        metaValues = [ float(x.split(':')[1]) for x in line[len(constituents)+1:] ]
        fFwlsKey = len(constituents) + len(metadatas) + 1
        for meta in metaValues:
            for const in constValues:
                fwlsSklFile.write(f' {fFwlsKey}:{meta * const:.10f}')
                fFwlsKey += 1
        fwlsSklFile.write('\n')
    streamFile.close()
    fwlsSklFile.close()


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    train = sys.argv[2]
    test = sys.argv[3]
    ignoreCB = False if len(sys.argv) <= 4 else sys.argv[4].lower() in [ "true", "t", "1" ]
    outputFold = f'{home}/features/F{train}-{test}'
    if not os.path.exists(outputFold): os.makedirs(outputFold)
    [constituents, keysFolds] = createHRFeatures(home, train, test, outputFold)
    metadatas = createSTREAMFeatures(home, train, test, outputFold, constituents, keysFolds)
    createFWLSFeatures(outputFold, constituents, metadatas, 'train', True)
    createFWLSFeatures(outputFold, constituents, metadatas, 'test', False)
    util.using("Fim")

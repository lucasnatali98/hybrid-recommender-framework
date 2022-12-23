'''
reifortes$
'''

import sys, os, glob
from pandas import DataFrame


def readFeatures(path, strategy):
    keys = {}
    features = {}
    keyFile = glob.glob(f'{path}/F????-?/{strategy}*.features')[0]
    keyFile = open(keyFile, 'r')
    for line in keyFile:
        line = line.strip().split(': ')
        keys[line[0]] = line[1]
    keyFile.close()
    featuresFiles = glob.glob(f'{path}/F????-?/{strategy}*.train')
    for file in featuresFiles:
        file = open(file, 'r')
        for line in file:
            line = line.strip().split(' ')
            for f in line[1:]:
                k, value = f.split(':')
                if keys[k] not in features: features[keys[k]] = []
                features[keys[k]].append(float(value))
        file.close()
    return DataFrame.from_dict(features)


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    dataSet      = sys.argv[1]
    featuresPath = f'{dataSet}/{sys.argv[2]}'
    strategy     = sys.argv[3]
    outPath      = f'{dataSet}/{sys.argv[4]}'
    if not os.path.exists(outPath): os.makedirs(outPath)
    data = readFeatures(featuresPath, strategy)
    outFile      = f'{outPath}/{strategy}.describe'
    #data.describe().transpose().to_csv(f'{outFile}.tsv','\t')
    data.describe().transpose().to_excel(f'{outFile}.xlsx', float_format="%.5f")
    data.describe().transpose().to_latex(f'{outFile}.tex', float_format="%.5f")
    print("Término")

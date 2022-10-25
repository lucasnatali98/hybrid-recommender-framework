'''
Plota gráfico de caracterização dos ratings das bases de dados.

reifortes$
'''

import sys, os, csv
import numpy as np
import matplotlib.pyplot as plt


def readRatings(fileName):
    uids = []
    iids = []
    values = []
    uidsMap = {}
    iidsMap = {}
    reader = csv.reader(open(fileName, 'r'), delimiter='\t')
    #test = 1
    for row in reader:
        uid = int(row[0])
        iid = int(row[1])
        if uid not in uidsMap: uidsMap[uid] = len(uidsMap) + 1
        if iid not in iidsMap: iidsMap[iid] = len(iidsMap) + 1
        uids.append(uidsMap[uid])
        iids.append(iidsMap[iid])
        values.append(float(row[2]))
        #test += 1
        #if test == 50: break
    print('Users:', len(set(uids)))
    print('Items:', len(set(iids)))
    return uids, iids, values


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    home   = sys.argv[1]
    basePath  = f'{home}/{sys.argv[2]}'
    inputFile = f'{basePath}/{sys.argv[3]}'
    outPath = f'{home}/{sys.argv[4]}'
    outFile = f'{outPath}/{sys.argv[5]}'

    if not os.path.exists(outPath): os.makedirs(outPath)
    x, y, values = readRatings(inputFile)
    plt.rcParams.update({'font.size': 8})
    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)
    n_bins = 20
    axs[0].hist(x, bins=n_bins)
    axs[0].set_xlabel('Users')
    axs[1].hist(y, bins=n_bins)
    axs[1].set_xlabel('Items')
    fig.tight_layout()
    plt.savefig(outFile)
    plt.close()
    print("Término")
'''
'''
import os.path
import sys, glob
import matplotlib.pyplot as plt
from util import StatsCalc
from util import createPath


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    print("Inicio")
    dataSet = sys.argv[1] # Bookcrossing
    resultsHome = f'{dataSet}/{sys.argv[2]}'
    outputHome = f'{dataSet}/{sys.argv[3]}'
    outputName = f'{outputHome}/{sys.argv[4]}'
    createPath(outputHome)
    files = glob.glob(f'{resultsHome}/*/*/*.tsv')
    results = {}
    print('- Processing files')
    for file in files:
        alg = os.path.basename(file).replace('.tsv', '')
        print(f'. Alg: {alg}')
        file = open(file, 'r')
        file.readline() # ignorando cabeçalho
        for line in file:
            line = line.strip().split('\t')
            Set = line[0]
            Seq = int(line[1])
            if Seq < 0: continue
            hv   = float(line[2].replace(',', '.')) if line[2] != '' else 0 # Hypervolume
            qtd  = float(line[3].replace(',', '.')) # Qtd solutions
            if Set not in results: results[Set] = {}
            if alg not in results[Set]: results[Set][alg] = {}
            if Seq not in results[Set][alg]: results[Set][alg][Seq] = (StatsCalc(), StatsCalc())
            results[Set][alg][Seq][0].update(hv)
            results[Set][alg][Seq][1].update(qtd)
    for Set in results:
        print(f'- {Set} Plots')
        fig = plt.figure()
        for alg in sorted(results[Set], key = len):
            print(f'. Alg: {alg}')
            x = [ k+1 for k in range(len(results[Set][alg])) ]
            y = []
            yerr = []
            for Seq in sorted(results[Set][alg]):
                hvMean, hvCI = results[Set][alg][Seq][0].calcIC()
                y.append(hvMean)
                yerr.append(hvCI)
            label = 'Risk-' if 'Risk' in alg else 'Rank'
            label += 'Traditional' if 'HR' in alg else 'Meta-featured'
            marker = ('o' if 'HR' in alg else 's') if 'Rank' in label else ('X' if 'HR' in alg else 'D')
            color  = 'gray' if 'HR' in alg else 'black'
            ecolor = 'lightgray' if 'HR' in alg else 'dimgray'
            plt.errorbar(x, y, yerr=yerr, label=label, marker=marker, color=color, ecolor=ecolor)
        plt.xlim([1, 25])
        plt.ylim([0.15, 0.39])
        plt.legend(loc='lower right')
        plt.savefig(f'{outputName}-{Set}.pdf')
        plt.close()
    print("Fim")

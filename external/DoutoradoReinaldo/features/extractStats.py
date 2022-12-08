import sys, glob, os
from pandas import read_csv
sys.path.insert(0, '/Users/reifortes/Downloads/temp/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


def statsForFiles(files, type, col, sep, ioFile):
    for file in sorted(files):
        name = os.path.basename(file).replace('.txt', '').replace('.tsv', '')
        ioFile.write(f'\n- {type}: {name}\n')
        dt = read_csv(file, sep=sep, usecols=[col])#, names=['valor'])
        ioFile.write(dt.describe().to_string()+'\n')
        #ioFile.write(f'NaN values: {dt["valor"].isna().sum()}\n')
        ioFile.write(f'NaN values: {dt.iloc[:,0].isna().sum()}\n')


def computeStats(home, fold, ioFile):
    ioFile.write(f'===============\nMetadata stats:\n===============\n')
    statsForFiles(glob.glob(f'{home}/Metadata/{fold}/*_Item.txt'), 'Metadata', 1, ';', ioFile)
    statsForFiles(glob.glob(f'{home}/Metadata/{fold}/*_User.txt'), 'Metadata', 1, ';', ioFile)
    ioFile.write(f'\n\n==================\nConstituent stats:\n==================\n')
    statsForFiles(glob.glob(f'{home}/constituent/{fold}/*.tsv'), 'Algorithm', 2, '\t', ioFile)


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    fold = sys.argv[2]
    featuresPath = f'{home}/features/{fold}'
    ioName = f'{featuresPath}/{sys.argv[3]}'
    if not os.path.exists(featuresPath): os.makedirs(featuresPath)
    ioFile = open(ioName, 'w')
    computeStats(home, fold, ioFile)
    ioFile.close()
    util.using("Fim")
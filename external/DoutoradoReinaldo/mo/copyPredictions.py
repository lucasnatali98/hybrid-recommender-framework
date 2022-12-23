'''
@author: reifortes
'''

import os,sys, glob
import shutil

def copyMFfiles(dataset, predictionsHome, outHome, r):
    files = []
    folds = glob.glob(f'{dataset}/{predictionsHome}/R{r}/*/')
    for fold in folds:
        fold = os.path.basename(fold[:-1])
        if dataset == 'Amazon':
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/hybrid/R{r}/{fold}/STREAM-all*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/MO_FWLS-sel_E-false_S-false*SOL-SUM*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/SO_STREAM-all_E-false*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/RISK_FWLS-sel-all_*E-false_S-false*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/RISK_SO_STREAM-all_*E-false*.sorted'))
        elif dataset == 'Bookcrossing':
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/hybrid/R{r}/{fold}/FWLS-all*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/MO_HR-sel_E-false_S-false*SOL-SUM*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/SO_FWLS-all_E-false*.sorted'))
        elif dataset == 'Jester':
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/hybrid/R{r}/{fold}/HR-sel*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/MO_HR-all_E-false_S-false*SOL-SUM*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/SO_HR-all_E-false*.sorted'))
        elif dataset == 'ML20M':
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/hybrid/R{r}/{fold}/STREAM-all*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/MO_STREAM-sel_E-false_S-false*SOL-SUM*.sorted'))
            files.extend(glob.glob(f'{dataset}/{predictionsHome}/R{r}/{fold}/SO_FWLS-all_E-false*.sorted'))
        outFold = f'{outHome}/R{r}/{fold}'
        if not os.path.exists(outFold): os.makedirs(outFold)
        for file in files:
            print(f'- File: {file}')
            shutil.copy(file, outFold)


if __name__ == '__main__':
    print("Inicio")
    dataSet         = sys.argv[1]
    strategy        = sys.argv[2]
    r1              = int(sys.argv[3])
    r2              = int(sys.argv[4])
    outHome         = f'{dataSet}/{sys.argv[5]}'
    for r in range(r1, r2+1):
        copyMFfiles(dataSet, f'{strategy}/Predictions', outHome, r)
    print("Fim")

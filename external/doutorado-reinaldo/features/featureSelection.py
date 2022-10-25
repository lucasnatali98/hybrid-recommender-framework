'''
Realiza a selecao de features a partir dos arquivos skl_all
@authors: reifortes

references:
- https://chrisalbon.com/machine_learning/feature_selection/drop_highly_correlated_features/
- https://stackoverflow.com/questions/17712163/pandas-sorting-columns-by-their-mean-value
- https://www.scipy-lectures.org/packages/statistics/index.html
- https://github.com/lmego/customer_segments/blob/master/customer_segments.ipynb (usar regressao para eliminar features)
'''

import sys
sys.path.insert(0, '/Users/reifortes/Downloads/temp/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')

import util
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split as Tts
from sklearn.linear_model import RidgeCV

#ignoring warnings
import warnings
warnings.filterwarnings("ignore")


def fillData(scikitInDir, fileIn):
    file = open('%s/%s-all.features' % (scikitInDir, fileIn), 'r')
    columns = []
    for line in file:
        line = line.strip().split(' ')
        colName = line[1].replace('.txt', '')
        columns.append(colName)
    file.close()
    file = open('%s/%s-all.train' % (scikitInDir, fileIn), 'r')
    data = []
    for line in file:
        line = line.strip().split(' ')
        row = []
        for col in range(1, len(columns)+1):
            value = float(line[col].split(':')[1])
            row.append(value)
        data.append(row)
    return pd.DataFrame(data, columns=columns)


def dropByCorrelation(dataset):
    output.write('\n\n*\n* Correlation:\n*\n')
    correlation = dataset.corr().abs()
    #correlation = dataset.reindex(dataset.var().sort_values().index, axis=1).corr().abs()  # reordenando para eliminar o que tiver a menor variancia
    upper = correlation.where(np.triu(np.ones(correlation.shape), k=1).astype(np.bool))
    upper.drop(columns=[upper.columns[0]], inplace=True)
    #output.write(upper.to_string(na_rep='-'))
    to_drop_byCorrelation = [column for column in upper.columns if any(upper[column] > 0.95)]
    output.write('\n\n- To Drop by Correlation > 0.95 (%d):  %s\n' % (len(to_drop_byCorrelation), str(to_drop_byCorrelation)))
    return to_drop_byCorrelation


''' 
The coefficient R^2 is defined as (1 - u/v), where u is the residual sum of squares ((y_true - y_pred) ** 2).sum() and v is the total sum of squares ((y_true - y_true.mean()) ** 2).sum(). 
The best possible score is 1.0 and it can be negative (because the model can be arbitrarily worse). 
A constant model that always predicts the expected value of y, disregarding the input features, would get a R^2 score of 0.0.
font: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html#sklearn.linear_model.RidgeCV.score
'''
def dropByRegression(recursive, dataset, cumulative, r2):
    output.write('\n\n*\n* Regression:\n*\n')
    to_drop_byRegression = []
    for response in dataset.columns:
        regData = dataset.drop(to_drop_byRegression + [response], axis=1).fillna(0) # replace nan with zero
        descriptors = regData.columns.tolist()
        #print('Response: %s\nDescriptors (%d): %s' % (response, len(descriptors), str(descriptors)))
        y = dataset[response].fillna(0) # replace nan with zero
        while len(descriptors) > 1:
            X_train, X_test, y_train, y_test = Tts(regData, y, test_size=0.25, random_state=30)
            regressor = RidgeCV(alphas=list(np.arange(0.0, 1, 0.05))+list(np.arange(1, 5.1, 0.2)), cv=5, fit_intercept=True)
            regressor.fit(X_train, y_train)
            score = regressor.score(X_test, y_test)
            if score >= r2:
                #print('Feature do drop: %s (R^2 = %.2f)' % (response, score))
                to_drop_byRegression.append(response)
                break
            # remover descritor com o coeficiente mais proximo de zero (apenas quando for recursivo)
            if not recursive: break
            index = min(range(len(regressor.coef_)), key=lambda i: abs(regressor.coef_[i]))
            regData.drop([ descriptors[index] ], axis=1, inplace=True)
            descriptors.remove(descriptors[index])
    output.write(f'\n\n- To Drop by Regression{" Cumulative" if cumulative else ""}{" Recursive" if recursive else ""} R^2 >= {r2} ({len(to_drop_byRegression)}): {str(to_drop_byRegression)}')
    return to_drop_byRegression


# https://github.com/oliviaguest/gini
def gini(array):
    """Calculate the Gini coefficient of a numpy array."""
    # based on bottom eq: http://www.statsdirect.com/help/content/image/stat0206_wmf.gif
    # from: http://www.statsdirect.com/help/default.htm#nonparametric_methods/gini.htm
    array = array[~np.isnan(array)]
    if len(array) == 0: return 0
    array = array.flatten() #all values are treated equally, arrays must be 1d
    if np.amin(array) < 0:
        array -= np.amin(array) #values cannot be negative
    array += 0.0000001 #values cannot be 0
    array = np.sort(array) #values must be sorted
    index = np.arange(1,array.shape[0]+1) #index per array element
    n = array.shape[0]#number of array elements
    return ((np.sum((2 * index - n  - 1) * array)) / (n * np.sum(array))) #Gini coefficient


def computeGiniValues(data):
    giniData = []
    for c in data.columns:
        g = gini(data[c].values)
        giniData.append(g)
    giniData = [ giniData ]
    giniValues = pd.DataFrame(giniData, columns=data.columns)
    return giniValues


def toDropByGini(giniValues, value):
    output.write('\n\n*\n* Variance:\n*\n')
    to_drop_byGini = [ column for column in data.columns if giniValues[column][0] < value ]
    output.write('\n\n- To Drop by Gini < %.2f (%d): %s\n' % (value, len(to_drop_byGini), str(to_drop_byGini)))
    return to_drop_byGini


def updateCumData(to_drop, dataset, cum):
    if cum:
        return dataset.drop(to_drop, axis=1)
    else:
        return dataset


def checkRemaining(dataset, cum):
    remaining = dataset.columns.tolist()
    return cum and len(remaining) == 0


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    util.using("Inicio")
    homeDir = sys.argv[1]  # /Users/reifortes/Downloads/temp/execution11/Bookcrossing
    fold = sys.argv[2] # F1234-5
    scikitDir = '%s/%s/%s' % (homeDir, sys.argv[3], fold) # features
    fileIn = sys.argv[4] # FWLS
    limits = [ float(x) for x in sys.argv[5].split(';') ] if len(sys.argv) > 5 else [ 0.05, 0.10, 0.15 ]
    r2s = [ float(x) for x in sys.argv[6].split(';') ] if len(sys.argv) > 6 else [ 0.25, 0.5, 0.75 ]
    cumulatives = [ x.lower() == 'true' for x in sys.argv[7].split(';') ] if len(sys.argv) > 7 else [ False, True ]
    outFileName = sys.argv[8] if len(sys.argv) > 8 else None
    data = fillData(scikitDir, fileIn)
    total = data.count().sum()
    data.mask(data < 0, axis=0, inplace=True)  # converting nan values
    smaller = data.isnull().values.sum()
    data.mask(data > 1, inplace=True)  # converting nan values
    bigger = data.isnull().values.sum() - smaller
    giniValues = computeGiniValues(data)
    all_to_drop = set()
    for limit in limits:
        print('- Limit: %.2f' % limit)
        for r2 in r2s:
            print('- R^2: %.2f' % r2)
            for cum in cumulatives:
                cumData = data.copy()
                fileName = outFileName if outFileName else f'G_{limit:.2f}_R_{r2:.2f}{"_Cum" if cum else ""}.selection'
                output = open(f'{scikitDir}/{fileIn}-{fileName}', 'w')
                to_drop = toDropByGini(giniValues, limit)
                all_to_drop = all_to_drop.union(set(to_drop))
                cumData = updateCumData(to_drop, cumData, cum)
                if not checkRemaining(cumData, cum):
                    to_drop = dropByCorrelation(cumData)
                    all_to_drop = all_to_drop.union(set(to_drop))
                    cumData = updateCumData(to_drop, cumData, cum)
                    if not checkRemaining(cumData, cum):
                        to_drop = dropByRegression(False, cumData, cum, r2)
                        all_to_drop = all_to_drop.union(set(to_drop))
                        cumData = updateCumData(to_drop, cumData, cum)
                output.close()
    util.using("Término")

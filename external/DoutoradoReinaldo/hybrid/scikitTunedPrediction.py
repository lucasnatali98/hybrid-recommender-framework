'''
Execute experiments based on the k-fold crossvalidation with Probe, Test and training partitions.

Created on 10/08/2015
Updated on 14/11/2015 (passing attributes files as 'none')
Updated on 17/02/2019
@author: reifortes

Command line: python2.7 scikitTunedPrediction.py /Users/reifortes/Downloads/temp/Execution05/ML-100K/Scikit-Norm/ SKL/ Fold-Valid/ Fold-Test-1/ keys/ H-NaN FWLS- Predictions/

References:
- http://scikit-learn.org/stable/index.html
-
'''

import warnings, importlib
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    import os
    import sys
    import time
    from datetime import datetime
    from sklearn.datasets import load_svmlight_file


def loadKeys(fileName):
    arq = open(fileName, 'r')
    keys = []
    for line in arq:
        keys.append(line.strip())
    return keys


def saveFile(outputPath, strategy, learningMethod, predictions, keys):
    if not os.path.exists(outputPath): os.makedirs(outputPath)
    outName = '%s%s-%s.tsv' % (outputPath, strategy, learningMethod)
    out = open(outName, 'w')
    for n in range(0, len(predictions)):
        out.write('%s,%.7f,0\n' % (keys[n], predictions[n]))
    out.close()


def saveCoeff(coefficientsFold, strategy, learningMethod, estimator):
    if not os.path.exists(coefficientsFold): os.makedirs(coefficientsFold)
    outName = '%s%s-%s.coef' % (coefficientsFold, strategy, learningMethod)
    out = open(outName, 'w')
    if hasattr(estimator, 'coef_'):
        out.write('coef_')
        # if estimator.coef_ != None:
        #    for c in estimator.coef_: out.write('\t%f' % (c))
        for c in estimator.coef_: out.write('\t%f' % (c))
        out.write('\nintercept_')
        # if estimator.intercept_ != None: out.write('\t%f' % ( estimator.intercept_))
        out.write('\t%.7f' % (estimator.intercept_))
    else:
        out.write('Estimator does not have attribute coef_')
    out.close()


if __name__ == '__main__':
    st = time.time()
    print("\nStarted")
    print(datetime.now())
    print("--------------\n")
    print(sys.argv)
    home             = sys.argv[1]
    scikitPath       = home + sys.argv[2]
    sklPath          = sys.argv[3]
    keysFile         = sys.argv[4]
    algorithmsKey    = sys.argv[5]
    strategy         = sys.argv[6]
    predictionsFold  = home + sys.argv[7]
    algorithmsFile   = sys.argv[8]
    #sys.path.append(os.path.dirname(algorithmsFile))#to import algorithmsConf
    #algorithmsConf   = __import__(algorithmsFile)# algorithms gerado por 'scikitTunedConfigs.py'
    algorithmsConf = importlib.import_module(algorithmsFile)

    print('- Predicting for algorithmsKey: %s ' % algorithmsKey)
    if algorithmsKey != 'none':
        path  = '%s%s%s/' % (scikitPath, sklPath, algorithmsKey)
    else:
        path  = '%s%s' % (scikitPath, sklPath)
        algorithmsKey = ''
    outputPath = '%s%s' % (predictionsFold, sklPath)
    print('sklPath..: %s' % sklPath)
    print('outputPath.: %s' % outputPath)
    print('-- Predicting for strategy: %s ' % strategy)
    print('--- Loading data')
    st_Load = time.time()
    TrainFeatures, TrainOuts = load_svmlight_file('%s%s.train' % (path, strategy))
    TestFeatures, TestOuts = load_svmlight_file('%s%s.test' % (path, strategy))
    keys = loadKeys('%s%s' % (path, keysFile))
    et_Load = time.time()
    ds_Load = et_Load - st_Load
    dm_Load = ds_Load / 60
    print('--- Finished in %2.2f sec / %2.2f min (EXE time).' % (ds_Load, dm_Load))
    learningMethod = type(algorithmsConf.algorithms[algorithmsKey]['%s.train' % strategy]).__name__
    print('--- Predicting: %s' % learningMethod)
    st_alg = time.time()
    estimator = algorithmsConf.algorithms[algorithmsKey]['%s.train' % strategy]
    print('---- Training')
    erro = False
    try:
        estimator.fit(TrainFeatures.toarray(), TrainOuts)
    except:
        print('----- Error on training, trying without toarray().')
        try:
            estimator.fit(TrainFeatures, TrainOuts)
        except:
            print('----- Error on training.')
            erro = True
    if not erro:
        print('---- Predicting')
        try:
            predictions = estimator.predict(TestFeatures.toarray())
        except:
            print('----- Error on predicting, trying without toarray().')
            try:
                predictions = estimator.predict(TestFeatures)
            except:
                print('----- Error on predicting.')
                erro = True
    if not erro:
        print('---- Saving predictions')
        saveFile(outputPath + algorithmsKey + '/', strategy, learningMethod, predictions, keys)
        saveCoeff(outputPath + algorithmsKey + '/', strategy, learningMethod, estimator)
    et_alg = time.time()
    ds_alg = et_alg - st_alg
    dm_alg = ds_alg / 60
    print('--- Finished in %2.2f sec / %2.2f min (EXE time).' % (ds_alg, dm_alg))

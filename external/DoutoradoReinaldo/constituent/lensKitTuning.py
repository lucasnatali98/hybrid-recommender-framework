import sys, os
from pandas import read_csv
from lenskit.algorithms import Recommender, basic, item_knn, user_knn, als, svd, tf, hpf
from lenskit.batch import predict
from lenskit.metrics.predict import rmse
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def createAlgorithm(alg):
    aldLow = alg.lower()
    if aldLow == 'bias':             return basic.Bias()
    if 'itemknn' in aldLow:          return item_knn.ItemItem(int(alg.split('-')[1]))
    if 'userknn' in aldLow:          return user_knn.UserUser(int(alg.split('-')[1]))
    if 'als_biasedmf' in aldLow:     return als.BiasedMF(int(alg.split('-')[1]))
    if 'implicitmf' in aldLow:       return als.ImplicitMF(int(alg.split('-')[1]))
    if 'biasedsvd' in aldLow:        return svd.BiasedSVD(int(alg.split('-')[1]))
    if 'tf_biasedmf' in aldLow:      return tf.BiasedMF(int(alg.split('-')[1]))
    if 'integratedbiasmf' in aldLow: return tf.IntegratedBiasMF(int(alg.split('-')[1]))
    if 'bpr' in aldLow:              return tf.BPR(int(alg.split('-')[1]))#pode gastar muita memória
    if 'hpf' in aldLow:              return hpf.HPF(int(alg.split('-')[1]))# no mac ainda nao roda (instalar hpfrec)


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    algName = sys.argv[2]
    train = sys.argv[3]
    test1 = sys.argv[4]
    test2 = sys.argv[5]
    cores = int(sys.argv[6])
    trainData = read_csv(f'{home}/BD/Sample{train}.train', sep='\t', usecols=[0,1,2], names=['user', 'item', 'rating'])#, 'timestamp'])
    alg = createAlgorithm(algName)
    alg = Recommender.adapt(alg)
    alg.fit(trainData)
    # test 1
    if test1:
        testData = read_csv(f'{home}/BD/Sample{test1}.test', sep='\t', usecols=[0,1,2], names=['user', 'item', 'rating'])#, 'timestamp'])
        preds = predict(alg, testData, n_jobs=cores)
        runsFolder = f'{home}/constituent/F{train}-{test1}'
        if not os.path.exists(runsFolder): os.makedirs(runsFolder)
        preds.to_csv(f'{runsFolder}/{algName}.tsv', sep='\t', index=False, columns=['user', 'item', 'prediction'])
        acc = rmse(preds['prediction'], preds['rating'])
        outFile = open(f'{runsFolder}/{algName}.eval.txt', 'w')
        outFile.write(f'rmse\t{acc}\n')
        outFile.close()
    # test 2
    if test2:
        testData = read_csv(f'{home}/BD/Sample{test2}.test', sep='\t', usecols=[0,1,2], names=['user', 'item', 'rating'])#, 'timestamp'])
        preds = predict(alg, testData, n_jobs=cores)
        runsFolder = f'{home}/constituent/F{train}-{test2}'
        if not os.path.exists(runsFolder): os.makedirs(runsFolder)
        preds.to_csv(f'{runsFolder}/{algName}.tsv', sep='\t', index=False, columns=['user', 'item', 'prediction'])
        acc = rmse(preds['prediction'], preds['rating'])
        outFile = open(f'{runsFolder}/{algName}.eval.txt', 'w')
        outFile.write(f'rmse\t{acc}\n')
        outFile.close()
    util.using("Fim")
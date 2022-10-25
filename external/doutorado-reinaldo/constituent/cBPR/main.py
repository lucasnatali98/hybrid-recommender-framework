import implicit
import pandas as pd
import sys, os
import numpy as np

dataset = sys.argv[1]
sampleTrain = sys.argv[2]
sampleTest = sys.argv[3]
predict_file = f'{dataset}/constituent/F{sampleTrain}-{sampleTest}/{sys.argv[4]}'
# Setup a dataframe from the CSV and make it sparse

# df = pd.read_csv('dummy/BD/sample70.train', sep="\t", usecols=[0, 1, 2], names=['userId',
#                    'movieID', 'ratings'])
# df_test = pd.read_csv('dummy/BD/sample70.test', sep="\t", usecols=[0, 1, 2], names=['userId',
#                    'movieID', 'ratings'])
#
df = pd.read_csv(dataset + '/BD/Sample' + sampleTrain + '.train', sep="\t", usecols=[0, 1, 2], names=['userId', 'movieID', 'ratings'])
df_test = pd.read_csv(dataset + '/BD/Sample' + sampleTest + '.test', sep="\t", usecols=[0, 1, 2], names=['userId', 'movieID', 'ratings'])

from scipy.sparse import csr_matrix
item_user_data = csr_matrix((df.ratings, (df.userId , df.movieID)))
item_user_data_test = csr_matrix((df_test.ratings, (df_test.userId , df_test.movieID)))

# initialize a model
# model = implicit.als.AlternatingLeastSquares(factors=50)
# model = implicit.bpr.BayesianPersonalizedRanking(iterations=2, factors=8, learning_rate=0.1)
# model = implicit.bpr.BayesianPersonalizedRanking(iterations=2, factors=16, learning_rate=0.1)
# model = implicit.bpr.BayesianPersonalizedRanking(iterations=2, factors=8, learning_rate=0.01)
# model = implicit.bpr.BayesianPersonalizedRanking(iterations=2, factors=16, learning_rate=0.01)
model = implicit.bpr.BayesianPersonalizedRanking(iterations=50, factors=int(sys.argv[5]), learning_rate=float(sys.argv[6]))

# train the model on a sparse matrix of item/user/confidence weights
model.fit(item_user_data)

# recommend items for a user
user_items = item_user_data.T.tocsr()

df_n = df_test.to_numpy()
all_rs = []
r_evals = []

r1 = []
r2 = []
for line in df_n:
    # recommendations = model.recommend(int(line[0]), user_items)
    try:
        r = model.rank_items(int(line[0]), item_user_data, [int(line[1])])[0][1]
        all_rs.append(r)
        r1.append(float(line[2]))
        r2.append(r)
    except:
        all_rs.append("")
    r_evals.append(float(line[2]))

predict_path = os.path.dirname(os.path.abspath(predict_file))
if not os.path.exists(predict_path): os.makedirs(predict_path)
f = open(predict_file, 'w+')
f.write("user\titem\tprediction\n")
cont = 0
evals = []
for line in df_n:
    f.write(str(line[0]) + "\t" + str(line[1]) + "\t" + str(all_rs[cont]) + "\n")
    cont += 1
f.close()


r_evals = np.array(r1).reshape(-1)
m_predictions = np.array(r2).reshape(-1)
r = m_predictions - r_evals
r = np.sqrt(np.mean(r * r))

f = open(predict_file.replace(".tsv", ".eval.txt"), 'w+')
f.write("rmse " + str(r) + "\n")
f.close()

#f = open(model_file, 'w+')
#f.close()


# amelia2
# nohup sh run/constituents/new_execConstituents.sh Amazon 4 4 70 4 1 1 > run_cbpr.log

# amelia1
# nohup sh run/constituents/new_execConstituents.sh ML20M 4 4 70 4 1 1 > run_cbpr.log
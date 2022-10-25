# dataset name
import sys

dataset1 = sys.argv[1]
sampleTrain = sys.argv[2] #sample
sampleTest = sys.argv[3]
predict_name = sys.argv[4]
my_path = sys.argv[5] #path to NCF

# print(my_path + "in blblblblblblbl")
# dataset = 'Amazontuning70'
dataset = dataset1 + sampleTrain
# assert dataset in ['ml-1m', 'pinterest-20']

# model name 
model = 'NeuMF-end'
assert model in ['MLP', 'GMF', 'NeuMF-end', 'NeuMF-pre']

# paths
# main_path = './NCF/data/'
main_path = my_path + "data/"

train_rating = main_path + '{}.train.rating'.format(dataset)
test_rating = main_path + '{}.test.rating'.format(dataset)
test_negative = main_path + '{}.test.negative'.format(dataset)

# model_path = './NCF/models/'
#model_path = model_name
# GMF_model_path = model_path + 'GMF.pth'
# MLP_model_path = model_path + 'MLP.pth'
# NeuMF_model_path = model_path + 'NeuMF.pth'

#GMF_model_path = model_path
#MLP_model_path = model_path
#NeuMF_model_path = model_path

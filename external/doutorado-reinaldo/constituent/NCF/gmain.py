import os
import time
import argparse
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import sys
dataset = sys.argv[1]
sample = sys.argv[2] #sample
model_name = sys.argv[3]
predict_name = sys.argv[4]
my_path = sys.argv[5] #path to NCF



import torch.backends.cudnn as cudnn
from tensorboardX import SummaryWriter

import model
import config
import gevaluate
import data_utils

parser = argparse.ArgumentParser()
parser.add_argument("--lr",
                    type=float,
                    default=0.001,
                    help="learning rate")
parser.add_argument("--dropout",
                    type=float,
                    default=0.0,
                    help="dropout rate")
parser.add_argument("--batch_size",
                    type=int,
                    default=256,
                    help="batch size for training")
parser.add_argument("--epochs",
                    type=int,
                    default=20,
                    help="training epoches")
parser.add_argument("--top_k",
                    type=int,
                    default=10,
                    help="compute metrics@top_k")
parser.add_argument("--factor_num",
                    type=int,
                    default=32,
                    help="predictive factors numbers in the model")
parser.add_argument("--num_layers",
                    type=int,
                    default=3,
                    help="number of layers in MLP model")
parser.add_argument("--num_ng",
                    type=int,
                    default=4,
                    help="sample negative items for training")
parser.add_argument("--test_num_ng",
                    type=int,
                    default=99,
                    help="sample part of negative items for testing")
parser.add_argument("--out",
                    default=True,
                    help="save model or not")
parser.add_argument("--gpu",
                    type=str,
                    default="0",
                    help="gpu card ID")
# args = parser.parse_args()
args, unknown = parser.parse_known_args()
# print(args)
os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
cudnn.benchmark = True

############################## PREPARE DATASET ##########################
train_data, test_data, user_num, item_num, train_mat = data_utils.load_all()

# construct the train and test datasets
train_dataset = data_utils.NCFData(
    train_data, item_num, train_mat, args.num_ng, True)
test_dataset = data_utils.NCFData(
    test_data, item_num, train_mat, 0, False)
train_loader = data.DataLoader(train_dataset,
                               batch_size=args.batch_size, shuffle=True, num_workers=4)
test_loader = data.DataLoader(test_dataset,
                              batch_size=args.test_num_ng + 1, shuffle=False, num_workers=0)

########################### CREATE MODEL #################################
if config.model == 'NeuMF-pre':
    assert os.path.exists(config.GMF_model_path), 'lack of GMF model'
    assert os.path.exists(config.MLP_model_path), 'lack of MLP model'
    GMF_model = torch.load(config.GMF_model_path)
    MLP_model = torch.load(config.MLP_model_path)
else:
    GMF_model = None
    MLP_model = None

model = model.NCF(user_num, item_num, args.factor_num, args.num_layers,
                  args.dropout, config.model, GMF_model, MLP_model)
model.cuda()
# model.cpu()
loss_function = nn.BCEWithLogitsLoss()

if config.model == 'NeuMF-pre':
    optimizer = optim.SGD(model.parameters(), lr=args.lr)
else:
    optimizer = optim.Adam(model.parameters(), lr=args.lr)


# writer = SummaryWriter() # for visualization

def predict_test_file(model):
    # currentdir = './NCF/'
    currentdir = my_path
    # dataset = "Amazon"
    # sample = "tuning70"
    usermap_FILE = open(currentdir + "data/ratings" + dataset + sample + ".usermap", "r")
    itemmap_FILE = open(currentdir + "data/ratings" + dataset + sample + ".itemmap", "r")

    user_map = {}
    item_map = {}

    for line in usermap_FILE:
        split_line = line.replace("\n", "").split("\t")
        user_map[int(split_line[0].split(".")[0])] = int(split_line[1].split(".")[0])

    for line in itemmap_FILE:
        split_line = line.replace("\n", "").split("\t")
        item_map[int(split_line[0].split(".")[0])] = int(split_line[1].split(".")[0])

    usermap_FILE.close()
    itemmap_FILE.close()

    # to_predict_file = open(args.datapath + args.dataset + "/BD/" + args.sample + ".test", "r")
    # main_path = './NCF/data/'
    main_path = './' + dataset + "/BD/"
    # to_predict_file = open("./" + dataset + "/BD/" + sample + ".test", "r")
    to_predict_file = open(main_path + sample + ".test", "r")
    m_users = []
    m_items = []

    i_users = []
    i_items = []

    evals = []
    for line in to_predict_file:
        v_u_i_r = line.replace("\n", "").split("\t")
        m_user, m_item, eval = int(v_u_i_r[0].split(".")[0]), int(v_u_i_r[1].split(".")[0]), float(v_u_i_r[2])
        m_users.append(m_user)
        m_items.append(m_item)

        if m_user in user_map and m_item in item_map:
            i_users.append(user_map[m_user])
            i_items.append(item_map[m_item])
            evals.append(eval)

    # predictions = model.predict([np.array(m_users), np.array(m_items)])
    # predictions = model.predict([np.array(i_users), np.array(i_items)])
    # predictions = model([np.array(i_users), np.array(i_items)])
    predictions = model(torch.from_numpy(np.array(i_users)), torch.from_numpy(np.array(i_items)))
    # f = open(model_out_file + ".predict", 'w+')
    # predictionfile = './NCF/test.model'
    predictionfile = predict_name
    savemodel = model_name
    f = open(predictionfile, 'w+')
    f.write("user\titem\tprediction\n")
    cont = 0
    predictions = predictions.detach().numpy()
    # predictions = predictions.cpu().detach().numpy()
    predictions = predictions.reshape(-1)
    print(predictions.shape)
    for ii in range(np.size(m_users)):
        if m_users[ii] in user_map and m_items[ii] in item_map:
            # f.write(str(m_users[ii]) + "\t" + str(m_items[ii]) + "\t" + str(round(predictions[cont][0], 4)) + "\n")
            f.write(str(m_users[ii]) + "\t" + str(m_items[ii]) + "\t" + str(round(predictions[cont], 4)) + "\n")
            cont += 1
        else:
            f.write(str(m_users[ii]) + "\t" + str(m_items[ii]) + "\t" + "\n")
    f.close()

    # f = open(model_out_file + ".eval.txt", 'w+')
    f = open(savemodel.replace(".model", "") + ".eval.txt", 'w+')
    predictions = np.array(predictions).reshape(-1)
    evals = np.array(evals).reshape(-1)
    r = predictions - evals
    r = np.sqrt(np.mean(r * r))
    f.write("rmse " + str(r) + "\n")
    f.close()


########################### TRAINING #####################################
count, best_hr = 0, 0

for epoch in range(args.epochs):
    print("running epoch {}".format(epoch))
    model.train()  # Enable dropout (if have).
    start_time = time.time()
    train_loader.dataset.ng_sample()
    my_count_epoch = 0
    for user, item, label in train_loader:
        user = user.cuda()
        # user = user.cpu()
        item = item.cuda()
        # item = item.cpu()
        label = label.float().cuda()
        # label = label.float().cpu()

        model.zero_grad()
        prediction = model(user, item)
        loss = loss_function(prediction, label)
        loss.backward()
        optimizer.step()
        # writer.add_scalar('data/loss', loss.item(), count)
        count += 1
        my_count_epoch += 1
        if my_count_epoch % 100 == 0:
            print("running " + str(my_count_epoch) + "/(train_loader.size)")

    model.eval()
    HR, NDCG = gevaluate.metrics(model, test_loader, args.top_k)

    elapsed_time = time.time() - start_time
    print("The time elapse of epoch {:03d}".format(epoch) + " is: " +
          time.strftime("%H: %M: %S", time.gmtime(elapsed_time)))
    print("HR: {:.3f}\tNDCG: {:.3f}".format(np.mean(HR), np.mean(NDCG)))

    if HR > best_hr:
        best_hr, best_ndcg, best_epoch = HR, NDCG, epoch

        if args.out:
            if not os.path.exists(config.model_path):
                os.mkdir(config.model_path)
            torch.save(model,
                       '{}{}.pth'.format(config.model_path, config.model))
        predict_test_file(model)

print("End. Best epoch {:03d}: HR = {:.3f}, NDCG = {:.3f}".format(
    best_epoch, best_hr, best_ndcg))

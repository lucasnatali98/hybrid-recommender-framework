import numpy as np
import time
import collections
import pandas as pd
import sys

_NUMBER_NEGATIVES = 100


#TODO: refatorar, é de uso geral, não apenas para movielens, e usa apenas ITEM_COLUMN, RATING_COLUMN, TIMESTAMP_COLUMN, USER_COLUMN
class movielens():
    GENRE_COLUMN = "genres"
    ITEM_COLUMN = "item_id"  # movies
    RATING_COLUMN = "rating"
    TIMESTAMP_COLUMN = "timestamp"
    TITLE_COLUMN = "titles"
    USER_COLUMN = "user_id"


def generate_train_eval_data(df, original_users, original_items, sample, current_dir):
    """Generate the dataset for model training and evaluation.
    Given all user and item interaction information, for each user, first sort
    the interactions based on timestamp. Then the latest one is taken out as
    Test ratings (leave-one-out evaluation) and the remaining data for training.
    The Test negatives are randomly sampled from all non-interacted items, and the
    number of Test negatives is 100 by default (defined as _NUMBER_NEGATIVES).
    Args:
      df: The DataFrame of ratings data.
      original_users: A list of the original unique user ids in the dataset.
      original_items: A list of the original unique item ids in the dataset.
    Returns:
      all_ratings: A list of the [user_id, item_id] with interactions.
      test_ratings: A list of [user_id, item_id], and each line is the latest
        user_item interaction for the user.
      test_negs: A list of item ids with shape [num_users, 100].
        Each line consists of 100 item ids for the user with no interactions.
    """
    # Need to sort before popping to get last item
    print("Sorting user_item_map by timestamp...")
    df.sort_values(by=movielens.TIMESTAMP_COLUMN, inplace=True)
    all_ratings = set(zip(df[movielens.USER_COLUMN], df[movielens.ITEM_COLUMN]))
    user_to_items = collections.defaultdict(list)
    # Generate user_item rating matrix for training
    t1 = time.time()
    row_count = 0
    for row in df.itertuples():
        user_to_items[getattr(row, movielens.USER_COLUMN)].append(
            getattr(row, movielens.ITEM_COLUMN))
        row_count += 1
        if row_count % 50000 == 0:
            print("Processing user_to_items row: {}".format(row_count))
    print("Process {} rows in [{:.1f}]s".format(row_count, time.time() - t1))
    # Generate test ratings and test negatives
    t2 = time.time()
    test_ratings = []
    test_negs = []
    # Generate the 0-based index for each item, and put it into a set
    all_items = set(range(len(original_items)))
    for user in range(len(original_users)):
        test_item = user_to_items[user].pop()  # Get the latest item id
        all_ratings.remove((user, test_item))  # Remove the test item
        all_negs = all_items.difference(user_to_items[user])
        all_negs = sorted(list(all_negs))  # determinism
        test_ratings.append((user, test_item))
        test_negs.append(list(np.random.choice(all_negs, _NUMBER_NEGATIVES)))
        if user % 1000 == 0:
            print("Processing user: {}".format(user))
    print("Process {} users in {:.1f}s".format(len(original_users), time.time() - t2))
    all_ratings = list(all_ratings)  # convert set to list
    # return all_ratings, test_ratings, test_negs
    # NEG_TEST_FILE = "./data/" + "ml-1m.test.negative"
    NEG_TEST_FILE = current_dir + "data/" + sample + ".test.negative"
    ff = open(NEG_TEST_FILE, 'w+')
    for l, t in zip(test_negs, test_ratings):
        ff.write("(")
        ff.write(str(t[0]))
        ff.write(",")
        ff.write(str(t[1]))
        ff.write(")")
        ff.write("\t")
        c = len(l)
        for i in range(c):
            if i == c - 1:
                ff.write(str(l[i]))
                ff.write("\n")
            else:
                ff.write(str(l[i]))
                ff.write("\t")
    ff.close()
    df.sort_values([movielens.USER_COLUMN, movielens.TIMESTAMP_COLUMN], ascending=[True, False], inplace=True)
    df_numpy = df.to_numpy()
    anterior = -999
    R_TEST_FILE = current_dir + "data/" + sample + ".test.rating"
    # R_TEST_FILE = "data/" + "ml-1m.test.rating"
    R_TRAIN_FILE = current_dir + "data/" + sample + ".train.rating"
    # R_TRAIN_FILE = "data/" + "ml-1m.train.rating"
    ff_train = open(R_TRAIN_FILE, 'w+')
    ff_test = open(R_TEST_FILE, 'w+')
    for rate in df_numpy:
        if rate[0] != anterior:
            anterior = rate[0]
            ff_test.write(str(rate[0]) + "\t" + str(rate[1]) + "\t" + str(rate[2]) + "\t" + str(rate[3]) + "\n")
        else:
            ff_train.write(str(rate[0]) + "\t" + str(rate[1]) + "\t" + str(rate[2]) + "\t" + str(rate[3]) + "\n")
    ff_test.close()
    ff_train.close()


if __name__ == '__main__':
    print('Parameters: ' + str(sys.argv))
    # home = sys.argv[1]
    # algName = sys.argv[2]
    # sample = sys.argv[3]
    # relevant = float(sys.argv[4])
    # cores = int(sys.argv[5])
    path_dataset = sys.argv[1]
    name_dataset = sys.argv[2]
    # bd = sys.argv[3]
    sample = sys.argv[3]
    current_dir = sys.argv[4]
    # ORIGINAL_RATINGS = path_dataset + name_dataset + "/" + bd + sample + ".train"
    ORIGINAL_RATINGS = path_dataset + "BD/Sample" + sample + ".train"
    RATINGS_FILE = current_dir + "data/ratings" + name_dataset + sample + ".csv"
    _MIN_NUM_RATINGS = 20
    # f = open('ratings.dat', 'r')
    f = open(ORIGINAL_RATINGS, 'r')
    fw = open(RATINGS_FILE, 'w+')
    fw.write(movielens.USER_COLUMN + "," + movielens.ITEM_COLUMN + "," + movielens.RATING_COLUMN + "," + movielens.TIMESTAMP_COLUMN + "\n")
    for line in f: fw.write(line.replace("::", ",").replace("\t", ","))
    fw.close()
    f.close()
    # df = movielens.ratings_csv_to_dataframe(data_dir=data_dir, dataset=dataset)
    df = pd.read_csv(RATINGS_FILE, encoding="utf-8")
    # Get the info of users who have more than 20 ratings on items
    grouped = df.groupby(movielens.USER_COLUMN)
    df = grouped.filter(lambda x: len(x) >= _MIN_NUM_RATINGS)
    original_users = df[movielens.USER_COLUMN].unique()
    original_items = df[movielens.ITEM_COLUMN].unique()
    # Map the ids of user and item to 0 based index for following processing
    print("Generating user_map and item_map...")
    user_map = {user: index for index, user in enumerate(original_users)}
    item_map = {item: index for index, item in enumerate(original_items)}
    usermap_FILE = open(current_dir+"data/ratings" + name_dataset + sample + ".usermap", "w+")
    itemmap_FILE = open(current_dir+"data/ratings" + name_dataset + sample + ".itemmap", "w+")
    for user in user_map:
        usermap_FILE.write(str(user) + "\t" + str(user_map[user]) + "\n")
    for item in item_map:
        itemmap_FILE.write(str(item) + "\t" + str(item_map[item]) + "\n")
    usermap_FILE.close()
    itemmap_FILE.close()
    df[movielens.USER_COLUMN] = df[movielens.USER_COLUMN].apply(lambda user: user_map[user])
    df[movielens.ITEM_COLUMN] = df[movielens.ITEM_COLUMN].apply(lambda item: item_map[item])
    assert df[movielens.USER_COLUMN].max() == len(original_users) - 1
    assert df[movielens.ITEM_COLUMN].max() == len(original_items) - 1
    original_df = pd.DataFrame(df)
    generate_train_eval_data(df, original_users, original_items, name_dataset + sample, current_dir)

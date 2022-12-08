import argparse, os, sys
import numpy as np
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util

util.using("Inicio")
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", type=str, required=True)
ap.add_argument("-s", "--sample", type=str, required=True)
ap.add_argument("-u", "--num_users", type=int, default=15000, required=False, help="users to select")
args = vars(ap.parse_args())
print('Parameters:', args)
old_file = args["dataset"] + "/BD/" + args["sample"] + ".test.all"
new_file = args["dataset"] + "/BD/" + args["sample"] + ".test"
os.rename(new_file, old_file)
keys = set()
with open(old_file) as file:
    for line in file:
        uid = int(line.split("\t")[0])
        keys.add(uid)
selected = np.random.choice(list(keys), args["num_users"], replace=False)
with open(old_file) as file:
    with open(new_file, 'w+') as wfile:
        for line in file:
            uid = int(line.split("\t")[0])
            if uid in selected:
                wfile.write(line)
util.using("Fim")

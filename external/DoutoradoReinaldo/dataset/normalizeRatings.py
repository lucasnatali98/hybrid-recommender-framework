import sys, csv
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util

# Rating values:
# Dataset       | min     | max     | Factor
# Jester        | 1.05    | 21.0    | 21.0
# Bookcrossing  | 1.0     | 10.0    | 10.0

if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    factor = float(sys.argv[2])
    inFile = f'{home}/BD/{sys.argv[3]}'
    outFile = f'{home}/BD/{sys.argv[4]}'
    inFile = open(inFile, 'r')
    outFile = open(outFile, 'w')
    ratings = csv.reader(inFile, delimiter='\t')
    ratingsNorm = csv.writer(outFile, delimiter='\t')
    for row in ratings:
        uid = int(row[0])
        iid = int(row[1])
        value = float(row[2])
        dt = int(row[3])
        ratingsNorm.writerow([uid, iid, value/factor, dt])
    inFile.close()
    outFile.close()
    util.using("Fim")

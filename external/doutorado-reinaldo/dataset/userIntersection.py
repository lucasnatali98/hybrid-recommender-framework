import sys
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util

def userIntersections(home):
    print('=====\nUsers\n=====')
    folds = [ 1, 2, 3, 4, 5 ]
    users = {}
    for x in folds:
        users[x] = set()
        file = open(f'{home}/BD/Sample{x}.test')
        for row in file:
            row = row.strip().split()
            uid = int(row[0])
            users[x].add(uid)
        print(f'{x}\t{len(users[x])}')
    for x in folds:
        print('---')
        unionY = set()
        for y in folds:
            if x == y: continue
            print(f'{x}.{y}\t{len(users[x].intersection(users[y]))}')
            unionY = unionY.union(users[y])
        print(f'UnionY\t{len(unionY)}')
        print(f'{x}.UnionY\t{len(users[x].intersection(unionY))}')


def userItemIntersections(home):
    print('\n===========\nUsers/Itens\n===========')
    folds = [ 1, 2, 3, 4, 5 ]
    usersItems = {}
    for x in folds:
        usersItems[x] = set()
        file = open(f'{home}/BD/Sample{x}.test')
        for row in file:
            row = row.strip().split()
            uid = int(row[0])
            iid = int(row[1])
            usersItems[x].add(f'{uid},{iid}')
        print(f'{x}\t{len(usersItems[x])}')
    for x in folds:
        print('---')
        unionY = set()
        for y in folds:
            if x == y: continue
            print(f'{x}.{y}\t{len(usersItems[x].intersection(usersItems[y]))}')
            unionY = unionY.union(usersItems[y])
        print(f'UnionY\t{len(unionY)}')
        print(f'{x}.UnionY\t{len(usersItems[x].intersection(unionY))}')


if __name__ == '__main__':
    util.using("Inicio")
    print('Parameters: ' + str(sys.argv))
    home = sys.argv[1]
    userIntersections(home)
    userItemIntersections(home)
    util.using("Fim")

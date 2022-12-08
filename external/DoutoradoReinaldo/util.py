'''
Copiar para as outras pastas se alterar esta classe, está dando erro nas máquinas do LBD
'''
import csv
import resource, gc
from datetime import datetime


def using(point=""):
    now = datetime.now()
    dtstr = now.strftime("%d/%m/%Y %H:%M:%S")
    usage = resource.getrusage(resource.RUSAGE_SELF)
    print('\n***** %s\n%s: usertime = %f; systime = %f; mem= %.2f' % (dtstr, point, usage[0], usage[1], (usage[2]*resource.getpagesize())/1000000.0))
    gc.collect()


def readUsers(ratingsFile):
    users = { }
    reader = csv.reader(open(ratingsFile), delimiter='\t')
    for row in reader:
        uid = int(row[0])
        if uid not in users: users[uid] = 1
        else: users[uid] += 1
    return users


def readItems(ratingsFile):
    items = { }
    reader = csv.reader(open(ratingsFile), delimiter='\t')
    for row in reader:
        iid = int(row[1])
        if iid not in items: items[iid] = 1
        else: items[iid] += 1
    return items
#!/usr/bin/env python -W ignore::DeprecationWarning
'''
Executar comandos de busca MO apenas para comandos que ainda não tenham sido executados
Necessário devido a erro na execução de ML20M, criado apenas para resolver este erro específico....

Created on 07/02/2016
Updated on 13/04/2017: ignore commented lines
@author: reifortes
'''

import sys, os, time, random
from threading import Thread
from queue import Queue, Empty
import util
queue = Queue()


def run_command(command):
    f = os.system(command)
    return f


class ExecuteThread(Thread):
    def run(self):
        st = time.process_time()
        global queue
        while True:
            try:
                command = queue.get()
                if command == None:
                    queue.put(None)
                    break
            except Empty:
                continue
            print("- %s: %s" % (self.getName(), command))
            run_command(command)
            queue.task_done()
            if queue.empty(): time.sleep(random.random())
        et = time.process_time()
        ds = et-st
        dm = ds / 60
        print("\n%s Finished in %2.2f sec / %2.2f min (CPU time)" % (self.getName(), ds, dm))


def readExecuted(executed, fileName):
    logFile = open(fileName, 'r')
    for line in logFile:
        if 'Total execution time' in line:
            line = line.strip().split('(')
            line = line[1].split(')')[0]
            executed.add(line)
    logFile.close()


if __name__ == '__main__':
    util.using("Inicio")
    st = time.time()
    print('Parameters: ' + str(sys.argv))
    commandsFile = open(sys.argv[1], "r")
    logFile = sys.argv[2]
    numberOfThreads = int(sys.argv[3])
    # reading executions
    executed = set()
    readExecuted(executed, logFile)
    readExecuted(executed, logFile.replace('.out', '.Pending.out'))
    # reading commands
    produced = 0
    for line in commandsFile:
        line = line.strip()
        if not line or line.startswith('#'): continue
        # eliminando execução SO
        if "run/MORecommenderSystem.jar PSO" in line: continue
        produce = True
        lineSplit = line.split('  ')
        p1 = lineSplit[4]
        p2 = lineSplit[8]
        for ex in executed:
            if p1 in ex and p2 in ex:
                produce = False
                break
        if produce:
            queue.put(line.replace('-Xmx30G', '-Xmx55G'))
            produced += 1
    commandsFile.close()
    queue.put(None)
    print("\nProduced %d commands.\n" % (produced))
    # creating threads
    consumers = []
    for i in range(0, min(numberOfThreads, produced)):
        consumer = ExecuteThread()
        consumers.append(consumer)
        consumer.start()
    # waiting threads
    for consumer in consumers:
        consumer.join()
    et = time.time()
    ds = et-st
    dm = ds / 60
    print("\nFinished in %2.2f sec / %2.2f min (EXE time)." %(ds, dm))
    util.using("Fim")

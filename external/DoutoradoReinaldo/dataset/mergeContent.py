'''
Agrega todos os campos em apenas um.
'''
import sys, html
sys.path.insert(0, '/Users/reifortes/Documents/tese/run/')
sys.path.insert(0, '/home/terralab/reinaldo/tese/run')
import util


if __name__ == '__main__':
    util.using("Inicio")
    home = sys.argv[1]
    inFile = f'{home}/BD/{sys.argv[2]}'
    outFile = f'{home}/BD/{sys.argv[3]}'
    inFile = open(inFile, 'r')
    outFile = open(outFile, 'w')
    for row in inFile:
        values = row.strip().split('|')
        iid = int(values[0])
        text = html.unescape(' '.join(values[1:]))
        outFile.write(f'{iid}|{text}\n')
    inFile.close()
    outFile.close()
    util.using("Fim")

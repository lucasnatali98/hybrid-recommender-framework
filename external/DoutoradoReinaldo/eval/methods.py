from util import getAlgName
import os, glob

class Method:
    name = ''
    category = ''
    combination = ''
    selection = ''
    measures = ''
    preference = ''
    statistics = ''
    decisionUser = ''
    decisionMeasure = ''
    def __init__(self, algName):
        self.getAttributes(algName)
    def getAttributes(self, algName):
        self.name = algName
        # Category
        if   algName.startswith('MO-'):     self.category = "MO"
        elif algName.startswith('SO-'):     self.category = "SO"
        elif algName.startswith('FWLS-'):   self.category = "WHF"
        elif algName.startswith('HR-'):     self.category = "WHF"
        elif algName.startswith('STREAM-'): self.category = "WHF"
        else:                               self.category = "Constituent"
        # Combination
        if   'FWLS-'   in algName: self.combination = 'FWLS'
        elif 'HR-'     in algName: self.combination = ' HR '
        elif 'STREAM-' in algName: self.combination = 'STREAM'
        else:                      self.combination = ''
        # Selection
        if   '-All' in algName: self.selection = 'All'
        elif '-Sel' in algName: self.selection = 'Sel'
        else:                   self.selection = ''
        # Measures
        if   '-Rank' in algName: self.measures = 'Rank'
        elif '-Risk' in algName: self.measures = 'Risk'
        else:                    self.measures = ''
        # Preference
        if   '-Weighted' in algName: self.preference = 'Weighted'
        elif '-Standard' in algName: self.preference = 'Standard'
        else:                        self.preference = ''
        # Statistics
        if   '-Stats'  in algName: self.statistics = 'Stats'
        elif '-Simple' in algName: self.statistics = 'Simple'
        else:                      self.statistics = ''
        # Decision Making - User
        if   '-IndRisk'    in algName: self.decisionUser = 'Ind'
        elif '-IndSUM'     in algName: self.decisionUser = 'Ind'
        elif '-SingleRisk' in algName: self.decisionUser = 'Single'
        elif '-SingleSUM'  in algName: self.decisionUser = 'Single'
        else:                         self.decisionUser = ''
        # Decision Making - Measure
        if   '-IndRisk'    in algName: self.decisionMeasure = 'Risk'
        elif '-IndSUM'     in algName: self.decisionMeasure = 'Sum'
        elif '-SingleRisk' in algName: self.decisionMeasure = 'Risk'
        elif '-SingleSUM'  in algName: self.decisionMeasure = 'Sum'
        else:                          self.decisionMeasure = ''
    def toString(self):
        return f'{self.name}\t{self.category}\t{self.combination.strip()}\t{self.selection}\t' \
               f'{self.measures}\t{self.preference}\t{self.statistics}\t' \
               f'{self.decisionUser}\t{self.decisionMeasure}'

class Methods:
    methods = []
    def __init__(self, foldPattern=None, fileName=None):
        self.methods = []
        if foldPattern != None:
            files = glob.glob(foldPattern)
            for file in files:
                file = os.path.basename(file)
                algName = getAlgName(file)
                self.methods.append(Method(algName))
        elif fileName != None:
            file = open(fileName, 'r')
            file.readline()
            file.readline()
            for line in file:
                line = line.strip().split()
                self.methods.append(Method(line[0]))
        self.sort()
    def sort(self):
        self.methods.sort(key=lambda x: x.decisionMeasure)
        self.methods.sort(key=lambda x: x.decisionUser)
        self.methods.sort(key=lambda x: x.statistics)
        self.methods.sort(key=lambda x: x.preference)
        self.methods.sort(key=lambda x: x.measures)
        self.methods.sort(key=lambda x: x.selection)
        self.methods.sort(key=lambda x: x.combination)
        self.methods.sort(key=lambda x: x.category)


#pattern = '/Users/reifortes/Documents/tese/Bookcrossing/Results/R1/F1234-5/N5/users/*.tsv'
#methods = Methods(foldPattern=pattern)
#fileName = '/Users/reifortes/Documents/tese/Bookcrossing/Results/Analisys/ranking_1_1_Metafeatured.tsv'
#methods = Methods(fileName=fileName)
#for method in methods.methods:
#    print(method.toString())

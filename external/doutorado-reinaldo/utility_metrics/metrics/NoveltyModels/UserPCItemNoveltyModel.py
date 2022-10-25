import math


class UserPCItemNovelty:
    # Nao preciso saber quem e o usr
    def __init__(self, recommenderData):  # dict[user_id] => [(item_id, value)]
        self.defaultReturnValue = 1.0
        self.itemNovelty = dict()
        for usr in recommenderData:
            for iv in recommenderData[usr]:
                if iv[0] not in self.itemNovelty: self.itemNovelty[iv[0]] = 0
                self.itemNovelty[iv[0]] += 1
        for i in self.itemNovelty:
            self.itemNovelty[i] = 1 - self.itemNovelty[i] / len(recommenderData)

    def novelty(self, iid):
        return self.itemNovelty[iid]

    def evaluationStart(self, uid):
        pass

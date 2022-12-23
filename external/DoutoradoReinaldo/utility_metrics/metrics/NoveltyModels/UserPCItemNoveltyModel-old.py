import math

class UserPCItemNovelty:
	#Nao preciso saber quem e o usr
	def __init__(self, recommenderData): # dict[user_id] => [(item_id, value)]
		self.defaultReturnValue = 1.0
		numUsers = 0
		itemsWithPreferences = set()
		self.itemNovelty = dict()
		for usr in recommenderData:
			numUsers += 1
			for iv in recommenderData[usr]:
				itemsWithPreferences.add(iv[0])
		for i in itemsWithPreferences:
			self.itemNovelty[i]= 1 - self.numUsers(recommenderData, i) / float(numUsers)

	def novelty(self, iid):
		return self.itemNovelty[iid]

	def numUsers(self, recommenderData, i):
		count = 0
		for uid in recommenderData.keys():
			for iv in recommenderData[uid]:
				if iv[0] == i:
					count += 1
		return count

	def evaluationStart(self, uid):
		pass

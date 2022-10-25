import math
import time

class NDCG:
	def __init__(self, cutoff, relModel):
		self.cutoff = cutoff
		self.relModel = relModel

	def evaluate(self, recommendation, user_id):
		self.relModel.evaluationStart(user_id)
		ndcg = 0.0
		rank = 0

		for pair in recommendation: #pair[0]=> id, pair[1]=> value
			ndcg += self.relModel.gain(pair[0]) * self.disc(rank)
			rank+=1
			if rank >= self.cutoff: break
		if ndcg > 0:
			ndcg /= self.idcg()
		return ndcg

	def idcg(self):
		gains = sorted(self.relModel.getGainValues())
		idcg = 0
		m = len(gains)
		n = min(self.cutoff, m)
		for rank in range(n):
			idcg += gains[m-rank-1] *self.disc(rank)
		return idcg

	def disc(self, k): #discount
		return 1 / math.log(k + 2.0) * math.log(2.0)
		
			

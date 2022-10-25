import math 

class ItemNoveltyMetric:
	def __init__(self, cutoff, relModel, noveltyModel, discModel):
		self.cutoff = cutoff
		self.relModel = relModel
		self.discModel = discModel
		self.noveltyModel = noveltyModel

	def evaluate(self, recommendation, user_id):
		self.relModel.evaluationStart(user_id)
		self.noveltyModel.evaluationStart(user_id)
		if self.noveltyModel is None: return 0.0
		
		nov = 0.0
		norm = 0.0

		rank = 0
		for iv in recommendation:
			nov += self.discModel.disc(rank)*self.relModel.gain(iv[0])*self.noveltyModel.novelty(iv[0])
			norm += self.discModel.disc(rank)
			rank+=1
			if rank >= self.cutoff: break
		if norm > 0.0:
			nov /= norm

		return nov

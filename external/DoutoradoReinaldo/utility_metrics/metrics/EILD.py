import math

class EILD:
	def __init__(self, cutoff, relModel, discModel, distanceModel):
		self.cutoff = cutoff
		self.relModel = relModel
		self.discModel = discModel
		self.distanceModel = distanceModel

	def evaluate(self, recommendation, user_id):
		self.relModel.evaluationStart(user_id)
		
		eild = 0.0
		norm = 0.0

		N = min(self.cutoff, len(recommendation))
		for i in range(N): 
			ieild = 0.0
			inorm = 0.0
			for j in range(N):
				if i == j: continue
				dist = self.distanceModel.distance(recommendation[i][0], recommendation[j][0])
				if not math.isnan(dist):
					w = self.discModel.disc(max(0, j-i-1)) * self.relModel.gain(recommendation[j][0])
				ieild += w * dist
				inorm += w
			if inorm > 0:
				eild += self.discModel.disc(i) * self.relModel.gain(recommendation[i][0]) * ieild / inorm
			norm = norm + self.discModel.disc(i)
		if norm > 0:
			eild /= norm
		return eild
			
			
		

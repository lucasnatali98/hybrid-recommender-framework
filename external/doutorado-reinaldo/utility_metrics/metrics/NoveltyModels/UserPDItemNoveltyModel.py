import math

class UserPDItemNovelty:
	def __init__(self, recommenderData, distanceModel): 
		if type(recommenderData) is dict: # dict[user_id] => [(item_id, value)]
			self.distanceModel = distanceModel
			self.recommenderData = recommenderData
			self.usrRecommenderData = None
		else:				  # [(item_id, value)] - um usr apenas
			self.distanceModel = distanceModel
			self.usrRecommenderData = recommenderData
			self.recommenderData = None
	
	def evaluationStart(self, uid): #selecao do usr correto, caso recommenderData seja global
		self.user_id = uid
		if not self.recommenderData is None:
			self.usrRecommenderData = self.recommenderData[self.user_id]

	def novelty(self, iid):
		items = [ i for i,v in self.usrRecommenderData ]
		distances = [ self.distanceModel.distance(iid, i) for i in items ]
		return sum([d/len(distances) for d in distances]) if len(distances) > 0 else 0.0
		
		
	

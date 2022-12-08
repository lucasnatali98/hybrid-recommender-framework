
class BaseUtilityMetric:
	def __init__(self):
		self.metric = metric

	def evaluate(self):
		raise NotImplementedError

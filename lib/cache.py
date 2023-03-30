from time import time


class Cache:
	def __init__(self, seconds: int=1):
		self.cache = None
		self.seconds = seconds
		self.updated = 0


	def get(self):
		return self.cache


	def should_update(self):
		t = time()
		diff = t - self.updated
		if diff >= self.seconds:
			self.updated = t
			return True
		return False
	

	def update(self, cache):
		self.cache = cache

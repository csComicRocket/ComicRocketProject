class PList:
	"""Stores the comics that need to be checked in each hour block."""
	def __init__(self):
		"""Pulls the needed data from storage."""
		self.items = [[[] for i in range(24)]for j in range(7)]
		#go through storage and append into the appropriate slot the urls in question
		
	def getSlot(self, timeSlot):
		"""Returns the set of comics for the given timeslot tuple"""
		return self.items[timeSlot[0]][timeSlot[1]]

if __name__ == "__main__":
	p = PList()
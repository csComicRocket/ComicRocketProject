import time

class ComicList:
	"""Represents a current list of pages in a comic that need to be checked.

	Keeps track of when the list of pages was last completely checked."""
	def __init__(self):
		"""Blind initialization will probably need to be replaced with a pull from storage."""	
		self.urls = []
		self.current = 0
		self.lastComplete = time.gmtime()
		
	def __init__(self, comicId):
		"""Given a comicId, retrieves the needed data from storage"""
		pass
		
	def getNext(self):
		"""Returns the next url to be checked or None if the list has been completed"""
		item = self.urls[self.current]
		self.current += 1
		if self.current == len(self.urls):
			self.current = 0
			self.lastComplete = time.gmtime()
			return None
		return item
		
class HistoryList:
	"""Contains the list of all comics to be checked.

	Has a list of comics that haven't reached the site limit and a list of comics waiting 
	until the next hour to resume."""
	def __init__(self):
		self.comics = []
		self.waiting = []
		
	def insertComic(self, data):
		"""Inserts a comic into the list based on the last completed time."""
		for i in xrange(len(self.comics)):
			if self.comics[i].lastComplete > data.lastComplete:
				self.comics.insert(i, data)
				return
		self.comics.append(data)
		return
	
	def getComic(self):
		"""Retrieves a comic from the list"""
		item = self.comics[0].getNext()
		while item == None:
			self.waiting.append(self.comics.pop(0))
			item = self.comics[0].getNext()
		return item
		
	def recoverWaiting(self):
		"""Adds the waiting comics back into the list."""
		while len(self.waiting) > 0:
			self.insertComic(self.waiting.pop(0))
		return
		
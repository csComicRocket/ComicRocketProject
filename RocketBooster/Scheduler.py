#Fredrik Fostvedt

import time
from PList import *
from ComicList import *
from Predictor import *

SITELIMIT = 20
PAGELIMIT = 20

def Scheduler():
	"""Checks the new comics expected in each hour block and the archived comics"""
	global histComics
	global newComics
	currentTime = time.gmtime().tm_wday, time.gmtime().tm_hour
	while (True):
		if time.gmtime().tm_hour != currentTime[1]:
			currentTime = time.gmtime().tm_wday, time.gmtime().tm_hour
			histComics.recoverWaiting()
			for comicId in newComics.getSlot(currentTime):
				
				# if newComicCheck(comicId), call predictor.update(comicId)
				pass
		#check histComics.getComic()
		
def loadData():
	"""Loads the data from storage into the histComics variable."""
	pass

histComics = HistoryList()
newComics = PList()
	
if __name__ == "__main__":
	Scheduler()
else:
	loadData()
	Scheduler()
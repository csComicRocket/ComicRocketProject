#Fredrik Fostvedt and Daniel Leblanc

import time
import os
import Predictor

SITELIMIT = 20
PAGELIMIT = 20

class ComicList:
    """Represents a current list of pages in a comic that need to be checked.

    Keeps track of when the list of pages was last completely checked."""
    def __init__(self):
        """Blind initialization will probably need to be replaced with a pull from storage."""	
        self.histData = ""
        self.urls = ""
        self.current = 0
        self.lastComplete = time.gmtime()
		
    def __init__(self, directory):
        """Given a comicId, retrieves the needed data from storage"""
        self.histData = directory + "historyData.txt"
        with open(self.histData) as f:
            data = f.readline()
            data = data.strip()
            self.lastComplete = time.strptime(data, gmtime())
            data = f.readline()
            data = data.strip()
            self.current = int(data)
        self.urls = directory + "historyList.txt"
		
    def getNext(self):
        """Returns the next url to be checked or None if the list has been completed"""
        with open(self.urls) as f:
            f.seek(self.current)
            item = f.readline()
            self.current = f.tell()
        if not item:
            self.current = 0
            self.lastComplete = time.gmtime()
            with open(self.histData, 'w+') as f:
                f.write(time.strftime(time.gmtime(), gmtime()) + '\n')
                f.write('0/n')
            return None
        with open(self.histData, 'w+') as f:
            f.write(time.strftime(self.lastComplete, gmtime()) + '\n')
            f.write(str(self.current) + '/n')
        return item.strip()
		
class HistoryList:
    """Contains the list of all comics to be checked.

    Has a list of comics that haven't reached the site limit and a list of comics waiting 
    until the next hour to resume."""
    def __init__(self):
        self.comics = []
        self.waiting = []
        
    def __init__(self, directories):
        self.comics = []
        for comic in directories:
            directory = '/Cache/cacheInfo/' + comic + '/'
            self.insertComic(ComicList(directory))
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

def scheduler():
    """Checks the new comics expected in each hour block and the archived comics"""
    histComics = HistoryList(os.listdir('Cache/cacheInfo/'))
    currentTime = time.gmtime().tm_wday, time.gmtime().tm_hour
    while (True):
        if time.gmtime().tm_hour != currentTime[1]:
            currentTime = time.gmtime().tm_wday, time.gmtime().tm_hour
            histComics.recoverWaiting()
            for comicId in Predictor.getCheckComicIds(currentTime):
                #if newComicCheck(comicId), call predictor.update(comicId)
                pass
		#check histComics.getComic()
		
def runTests():
    pass

if __name__ == "__main__":
    runTests()

#Daniel Leblanc

import time
import os
import threading
import Predictor
import F1Engine.checkComic

SITELIMIT = 20
PAGELIMIT = 20
SECONDS = 60

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
            self.lastComplete = time.strptime(data, time.gmtime())
            data = f.readline()
            data = data.strip()
            self.current = int(data)
        self.urls = directory + "historyList.txt"
		
    def getNext(self):
        """Returns the next url to be checked or None if the list has been completed"""
        urlList = []
        end = False
        with open(self.urls) as f:
            f.seek(self.current)
            for i in range(SITELIMIT):
                urlList.append(f.readline().strip())
                if not urlList[i]:
                    end = True
            self.current = f.tell()
        if end:
            self.current = 0
            self.lastComplete = time.gmtime()
        with open(self.histData, 'w+') as f:
            f.write(time.strftime(self.lastComplete, time.gmtime()) + '\n')
            f.write(str(self.current))
        return urlList
		
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
        urlList = self.comics[0].getNext()
        while len(urlList) == 0:
            self.waiting.append(self.comics.pop(0))
            urlList = self.comics[0].getNext()
        self.waiting.append(self.comics.pop(0))
        return urlList
		
    def recoverWaiting(self):
        """Adds the waiting comics back into the list."""
        while len(self.waiting) > 0:
            self.insertComic(self.waiting.pop(0))
        return

def scheduler():
    """Checks the new comics expected in each hour block and the archived comics"""
    global histComics
    Predictor.scanDirectories()
    histComics = HistoryList(os.listdir('Cache/cacheInfo/'))
    currentTime = time.gmtime().tm_wday, time.gmtime().tm_hour
    t = time.Timer((60-time.gmtime().tm_minute)*SECONDS, hourlyEvents)
    t.start()
    while (True):
        urlList = histComics.getComic()
        for url in urlList:
            F1Engine.checkComics.histCheck(url)
        
def hourlyEvents():
    global histComics
    currentTime = time.gmtime().tm_wday, time.gmtime().tm_hour
    histComics.recoverWaiting()
    for comicId in Predictor.getHourList(currentTime):
        directory = "../../cache/predictorInfo/" + str(comicId) + "/last3Pages.txt"
        urls = []
        with open(directory) as f:
            for line in f:
                urls.append(line.strip())
        for url in urls:
            F1Engine.checkComics.newComic(url)
    t = time.Timer((60-time.gmtime().tm_minute)*SECONDS, hourlyEvents)
    t.start()
		
def runTests():
    pass
    
histComics = Historylist()

if __name__ == "__main__":
    runTests()

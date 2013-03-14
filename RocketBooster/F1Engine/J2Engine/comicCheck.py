# Eric Smith & Daniel Leblanc

from compare import *
from fetchWeb import *
from cache import *
from notification import *
from LunarModule.pageTree import *
import Scheduler

#The only difference between these two functions at the moment is that the newComic func stores the new find in the cache
def newComic(comicURLs):
    lastChange = None
    for url in comicURLs:
        cache = Cache()
        webObject = fetchWeb(url,False)
        cacheObject = cache.fetchCache(url,None)
        if not compare(webObject, cacheObject):
            cache.storeCache(webObject)
            lastChange = url
    if lastChange:
        Scheduler.newComicNotification += 1
        notification("New: " + lastChange)
    return None

def histComic(comicURL):
    webObject = fetchWeb(comicURL,False)
    cache = Cache()
    cacheObject = cache.fetchCache(comicURL,None)
    if not compare(webObject, cacheObject):
        cache.storeCache(webObject)
        Scheduler.histComicNotification += 1
        notification("Hist: " + comicURL)
    return None

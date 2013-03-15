# Eric Smith & Daniel Leblanc

from compare import *
from fetchWeb import *
from cache import *
from notification import *
from LunarModule.pageTree import *
import Scheduler

#The only difference between these two functions at the moment is that the newComic func stores the new find in the cache
def newComic(comicURLs, comicId):
    lastChange = None
    for url in comicURLs:
        cache = Cache()
        lists = cache.getLists(url, comicId)
        webObject = fetchWeb(url, lists["BlackList"])
        cacheObject = cache.fetchCache(url,None)
        if not compare(webObject, cacheObject, lists["FilterList"]):
            cache.storeCache(webObject)
            lastChange = url
    if lastChange:
        Scheduler.newComicNotification += 1
        notification("New: " + lastChange)
    return None

def histComic(comicURL):
    cache = Cache()
    lists = cache.getLists(url)
    webObject = fetchWeb(comicURL, lists["BlackList"])
    cacheObject = cache.fetchCache(comicURL,None)
    if not compare(webObject, cacheObject, lists["FilterList"]):
        cache.storeCache(webObject)
        Scheduler.histComicNotification += 1
        notification("Hist: " + comicURL)
    return None

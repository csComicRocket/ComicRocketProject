# Eric Smith

from compare import *
from fetchWeb import *
from cache import *
from notification import *
from LunarModule.pageTree import *

"""def comicCheck(comicURL):
    webObject = fetchWeb(comicURL,False)
    cacheObject = fetchCache(comicURL,None)
    if compare(webObject.getHash(),cacheObject.getHash()) == False:
        storeCache(webObject)
        notification(comicURL)               
    return None
"""

#The only difference between these two functions at the moment is that the newComic func stores the new find in the cache
def newComic(comicURLs):
    lastChange = None
    for url in comicURLs:
        cache = Cache()
        webObject = fetchWeb(url,False)
        cacheObject = cache.fetchCache(url,None)
        if not compare(webObject, cacheObject):
            print "New Comic check testing: " + url
            cache.storeCache(webObject)
            lastChange = url
    if lastChange:
        notification(lastChange)
        #notification("New: " + lastChange)
    return None

def histComic(comicURL):
    #IN PROGRESS
    webObject = fetchWeb(comicURL,False)
    cache = Cache()
    cacheObject = cache.fetchCache(comicURL,None)
    if not compare(webObject, cacheObject):
        print "Hist Comic check testing: " + comicURL
        cache.storeCache(webObject)
        #notification("Hist: " + comicURL)
    return None

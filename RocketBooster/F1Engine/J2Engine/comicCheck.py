# Eric Smith

from compare import *
from fetchWeb import *
from cache import *
from notification import *
from LunarModule.pageTree import *

def comicCheck(comicURL):
    webObject = fetchWeb(comicURL,False)
    cacheObject = fetchCache(comicURL,None)
    if compare(webObject.getHash(),cacheObject.getHash()) == False:
        storeCache(webObject)
        notification(comicURL)
               
    return None


#The only difference between these two functions at the moment is that the newComic func stores the new find in the cache
'''def newComic(comicURL):
    webObject = fetchWeb(comicURL,False)
    cacheObject = fetchCache(comicURL,None)
    if compare(webObject.getHash(),cacheObject.getHash()) == False:
        storeCache(webObject)
        notification(comicURL)
               
    return None

def histComic(comicURL):
    #IN PROGRESS
    webObject = fetchWeb(comicURL,False)
    cacheObject = fetchCache(comicURL,None)
    if compare(webObject.getHash(),cacheObject.getHash()) == False:
        notification(comicURL)
    return None'''

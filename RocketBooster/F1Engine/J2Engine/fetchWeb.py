# Lucas Berge 2013

import LunarModule.pageTree
import errorNotification
#import urllib.request
#import urllib.error
import urllib2
from bs4 import BeautifulSoup

(_CACHE, _WEB) = range(2)
    
    
""" fillNode(response:urllib.response, comicNum:int, nodeNum:int, parentNum:int)
    Takes a non-error response, parses the content and puts it into and adds a node
    to the pageTree object """
def fillNode(rsp, comicNum, nodeNum=None, parentNum=None):        #comicID argument
    pageStr    = rsp.read()
    headerDict = rsp.info()
    soup = BeautifulSoup(pageStr)
    
    contentType = headerDict["Content-Type"]
    rspDate     = headerDict["Date"]
    mimeType    = headerDict["MIME-Version"]    #MIME and contentType appear to be the same thing
    
    tree.createPageNode(url, nodeNum, parentNum, _WEB, pageStr, contentType, rspDate)
    tree.setComicId(comicNum)
    if mimeType == None:                            #MIME and ContentType are interchangeable
        tree.setMimeType(0, contentType)
    else:
        tree.setMimeType(0, mimeType)
    #tree.setAuthorTS()
    #tree.setHash()

def handleError(e):
    #print e.code()
    print e.read()
    #errorNotification(e)
    
""" fetchWeb(url:string, imgs:boolean=None, comicID:int=None)
fetches requested URL from web, parses it and returns it in a PageTree object.
imgs is a boolean that specifies whether to retrieve the whole image or just headers
"""
def fetchWeb(url, comicID, imgs=None):
                
    tree   = LunarModule.pageTree.PageTree(None)
    nodeID = 0
        
    try:
        rsp  = urllib2.urlopen(url)                                        
        fillNode(rsp, comicID, nodeID, None)            # Fill root node # !!!comicID argument!!!
        soup = BeautifulSoup(rsp.read())
        
        for a in soup.findAll('a',href=True):            #Process links
            nodeID += 1
            rsp = urllib2.urlopen(a)
            fillNode(rsp, comicID, nodeID, 0)        
                
        for b in soup.findAll('img',href=True):            #Process Imgs
            nodeID += 1
            rsp = urllib2.urlopen(b)
            fillNode(rsp, comicID, nodeID, 0)
    except urllib2.HTTPError, e:
        handleError(e)
    
    return tree
    

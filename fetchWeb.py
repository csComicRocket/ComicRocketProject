# Lucas Berge 2013

import pageTree
import urllib.request
import urllib.error
from bs4 import BeautifulSoup

(_CACHE, _WEB) = range(2)
	
	
""" fillNode(response:urllib.response, comicNum:int, nodeNum:int, parentNum:int)
    Takes a non-error response, parses the content and puts it into and adds a node
    to the pageTree object """
def fillNode(response, comicNum=None, nodeNum=None, parentNum=None):		#comicID argument
	pageStr    = rsp.read()
	headerDict = rsp.info()
	soup = BeautifulSoup(pageStr)
	
	contentType = headerDict["Content-Type"]
	rspDate     = headerDict["Date"]
	mimeType    = headerDict["MIME-Version"]	#MIME and contentType appear to be the same thing
	
	tree.createPageNode(url, nodeNum, parentNum, _WEB, pageStr, contentType, rspDate)
	tree.setComicId(comicNum)
	if mimeType == None:							#MIME and ContentType are interchangeable
		tree.setMimeType(0, contentType)
	else:
		tree.setMimeType(0, mimeType)
	#tree.setAuthorTS()
	#tree.setHash()

	
""" fetchWeb(url:string, imgs:boolean=None, comicID:int=None)
fetches requested URL from web, parses it and returns it in a PageTree object.
imgs is a boolean that specifies whether to retrieve the whole image or just headers
"""
def fetchWeb(url, imgs=None, comicID=None):			# !!!comicID argument!!!
#comicID is implemented as an optional argument until another lookup method is devised
	tree   = PageTree(None)
	nodeID = 0
		
	# Root setup differs from leaf setup
	rsp  = urllib.request.urlopen(url)
	try:										
		fillNode(rsp, comicID, nodeID, None)			# Fill root node # !!!comicID argument!!!
	except urllib.error.HTTPError, e:
		print e.code()
		print e.read()
		tree.setContent(0, e.read, e.code)		# Set root's Content = error_header; EncodeType = error_code
		return tree								# HTTP error on root node; break early
	# End of root setup
	
	soup = BeautifulSoup(rsp.read())
		
	for a in soup.findAll('a',href=True, img=True):
		nodeID += 1
		rsp     = urllib.request.urlopen(req)
		try:										# if Success
			fillNode(rsp, comicID, nodeID, 0)		# !!!comicID argument!!!
		except urllib.error.HTTPError, e:			# if Failure
			print e.code()						
			print e.error()
			hDict = rsp.info()
			tree.createPageNode(url, nodeID, 0, _WEB, e.error, e.code, hDict["Date"])
	
	return tree
	

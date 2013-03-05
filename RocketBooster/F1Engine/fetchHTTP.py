#Lucas Berge
from J2Engine.fetchWeb import fetchWeb
from J2Engine.cache import Cache

def fetchHTTP(url, comicID, imgs=None):
	""" Checks cache for URL, if none, call fetchWeb. Returns PageTree"""
	pt = Cache.fetchCache(url)
	if (pt is None):
		pt = fetchWeb(url, comicID)	

if __name__ == "main":
	fetchHTTP()
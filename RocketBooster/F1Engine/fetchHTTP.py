#Lucas Berge
import J2Engine.fetchWeb
from J2Engine.cache import Cache

def fetchHTTP(url, comicID, imgs=None):
	""" Checks cache for URL, if none, call fetchWeb. Returns PageTree"""
    cache = Cache()
	pt = cache.fetchCache(url)
	if (pt is None):
		pt = fetchWeb.fetchWeb(url, comicID)	

if __name__ == "main":
	fetchHTTP()

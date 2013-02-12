#Lucas Berge
import J2Engine.fetchWeb
from J2Engine.cache import Cache

def fetchHTTP(url, imgs=None):
	""" Checks cache for URL, if none, call fetchWeb. Returns PageTree"""
	try:
		pt = Cache.fetchCache(url)
	except IOError:
		pt = fetchWeb.fetchWeb(url)
		
	return pt	

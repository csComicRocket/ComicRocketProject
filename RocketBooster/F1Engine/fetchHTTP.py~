#Lucas Berge
import J2Engine.fetchWeb
from J2Engine.cache import Cache

def fetchHTTP(url, comicID, imgs=None):
    """ Checks cache for URL, if none, call fetchWeb. Returns PageTree"""
    cache = Cache()
    url = "http://" + url
    pt = cache.fetchCache(url)
    if not pt:
        pt = J2Engine.fetchWeb.fetchWeb(url, comicID)
        cache.storeCache(pt)
    return pt

if __name__ == "main":
    fetchHTTP()

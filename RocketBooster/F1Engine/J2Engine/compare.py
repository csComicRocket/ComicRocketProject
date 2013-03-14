#Eric Smith & Daniel Leblanc

from LunarModule.pageTree import *

def compare(webPage, cachePage):
    applyFilters(webPage)
    applyFilters(cachePage)
    return linkCompare(webPage, cachePage)

def hashCompare(webPage, cachePage):
    """Compares a hash on the contents of the two pageTrees"""
    if(hash(cachePage.getContent(0)) == hash(webPage.getContent(0))):
        return True
    else:
        return False

def linkCompare(webPage, cachePage):
    """Compares the links used in the two pageTrees"""
    if len(cachePage.links) == len(webPage.links):
        for i in range(len(cachePage.links)):
            if cachePage.links[i] != webPage.links[i]:
                return False
    else:
        return False
    return True

def applyFilters(page):
    pass

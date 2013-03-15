#Eric Smith & Daniel Leblanc

from LunarModule.pageTree import *
import re

def compare(webPage, cachePage, linkFilters=[]):
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

def filteredLinkCompare(webPage, cachePage, linkFilters):
    for link in webPage.links:
        for exp in linkFilters:
            if re.search(exp, link) and link not in cachePage.links:
                return False
    return True


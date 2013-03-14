#Eric Smith & Daniel Leblanc

from LunarModule.pageTree import *

def hashCompare(webPage, cachePage):
    """Compares a hash on the contents of the two pageTrees"""
    if(hash(oldPage.getContent(0)) == hash(newPage.getContent(0))):
        return True
    else:
        return False

def compare(webPage, cachePage):
    """Compares the links used in the two pageTrees"""
    if len(oldPage.links) == len(newPage.links):
        for i in range(len(oldPage.links)):
            if i not in oldPage.blackList:
                if oldPage.links[i] != newPage.links[i]:
                    print "links mismatch: ", oldPage.links[i], newPage.links[i]
                    return False
    else:
        return False
    return True

def domainCompare(webPage, cachePage):
    """Just compares the Domains that have been reported as important"""
    for domain in cachePage.assocDomains:
        pass

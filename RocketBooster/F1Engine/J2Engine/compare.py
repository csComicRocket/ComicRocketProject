#Eric Smith

from LunarModule.pageTree import *

def compare(oldPage,newPage):
    if(oldPage.getHash() == newPage.getHash()):
        return True
    else:
        return False

def linkCompare(oldPage,newPage):
    if len(oldPage.links) == len(newPage.links):
        for i in xrange(len(oldPage.links)):
            if i not in oldPage.blacklist:
                if oldPage.links[i] != newPage.links[i]:
                    return False
    else:
        return False
    return True

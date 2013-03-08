#Eric Smith

from LunarModule.pageTree import *

def compare(newPage, oldPage):
    if(oldPage.getHash() == newPage.getHash()):
        return True
    else:
        return False

def linkCompare(newPage, oldPage):
    #print "old:", str(oldPage.links)
    #print "new:", str(newPage.links)
    if len(oldPage.links) == len(newPage.links):
        for i in xrange(len(oldPage.links)):
            if i not in oldPage.blackList:
                if oldPage.links[i] != newPage.links[i]:
                    return False
    else:
        return False
    return True

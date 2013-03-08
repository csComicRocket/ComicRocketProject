#Eric Smith

from LunarModule.pageTree import *

def hashCompare(oldPage,newPage):
    if(oldPage.getHash() == newPage.getHash()):
        return True
    else:
        return False

def compare(oldPage,newPage):
    print "old:", oldPage
    print "new:", newPage
    if len(oldPage.links) == len(newPage.links):
        for i in xrange(len(oldPage.links)):
            if i not in oldPage.blackList:
                if oldPage.links[i] != newPage.links[i]:
                    return False
    else:
        return False
    return True

#Eric Smith

from LunarModule.pageTree import *

def hashCompare(newPage, oldPage):
    if(hash(oldPage.getContent(0)) == hash(newPage.getContent(0))):
        return True
    else:
        return False

def compare(newPage, oldPage):
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

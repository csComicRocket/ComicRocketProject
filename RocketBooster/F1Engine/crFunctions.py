"""All functions in this method must have take a single argument which is a comma
delimited string.  They must split the string if they take more than one argument 
and change them into the form it needs.
"""

from J2Engine.cache import *
import Scheduler
import json

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def resetPredData(argList):
    """Reset the predictor history to default settings.
    
    argList should be a comic id"""
    try:
        comicId = int(argList)
    except ValueError:
        return False
    defaultPredData(comicId)
    return True
    
def lockPredData(comicId):
    """Lock a comics expected update schedule.
    
    argList should be a comic id
    Use this if a comic is going on hiatus and you want to avoid the predictor
    data losing accuracy."""
    Scheduler.lockComic(comicId, True)
    return False
    
def unlockPredData(comicId):
    """Unlock a comics expected update schedule.
    
    argList should be a comic id"""
    Scheduler.lockComic(comicId, False)
    return False
    
def setUpdateSchedule(comicId, data):
    """Set a comics update schedule to provided times.
    
    argList should be a comicId and a list of (day,hour) tuples"""

    #Not currently implemented
    return False

def invalidNotification(url):
    """Blacklists changes that produced an invalid notification"""
    cache = Cache()
    curTree = cache.fetchCache(url)
    lastTree = cache.fetchCache(url, -1)
    if len(curTree.links) != len(lastTree.links):
        return
    for i in range(len(curTree.links)):
        if curTree.links[i] != lastTree.links[i]:
            curTree.blackList.append(i)
    cache.storeCache(curTree)

def newComicFilterList(comicId, data):
    fname = cwd + "../Cache/predictorInfo/" + str(comicId) + "/filterData.txt"
    applyDataToStoredLists(fname, 'Filterlist', fname)

def newComicBlackList(comicId, data):
    fname = cwd + "../Cache/predictorInfo/" + str(comicId) + "/filterData.txt"
    applyDataToStoredLists(fname, 'BlackList', fname)

def histComicFilterList(url, data):
    pass

def histComicBlackList(url, data):
    pass

def applyDataToStoredLists(fname, key, data):
    try:
        data = json.loads(data)
        with open(fname) as f:
            lists = json.loads(f.read())
        for item in data[key]:
            lists[key].append(item)
        with open(fname, 'w+') as f:
            f.write(json.dump(lists))
    except ValueError, IOError:
        print "Invalid filter data"
        F1Engine.J2Engine.notification.notification("Invalid filter data")

def runTests():
    tests = []
    try:
        tests.append(("crFunctions.restPredData",1,resetPredData("1101")))
    except:
        tests.append(("crFunctions.restPredData",1,False))
    try:
        tests.append(("crFunctions.restPredData",2,not resetPredData("bob")))
    except:
        tests.append(("crFunctions.restPredData",2,False))
    try:
        tests.append(("crFunctions.restPredData",3,lockPredData("1101")))
    except:
        tests.append(("crFunctions.restPredData",3,False))
    try:
        tests.append(("crFunctions.restPredData",4,not lockPredData("bob")))
    except:
        tests.append(("crFunctions.restPredData",4,False))
    try:
        tests.append(("crFunctions.restPredData",5,unlockPredData("1101")))
    except:
        tests.append(("crFunctions.restPredData",5,False))
    try:
        tests.append(("crFunctions.restPredData",6,not unlockPredData("bob")))
    except:
        tests.append(("crFunctions.restPredData",6,False))
    try:
        tests.append(("crFunctions.restPredData",7,setUpdateSchedule("1101, [(1,1),(2,2)]")))
    except:
        tests.append(("crFunctions.restPredData",7,False))
    try:
        tests.append(("crFunctions.restPredData",8,not setUpdateSchedule("bob, invalid")))
    except:
        tests.append(("crFunctions.restPredData",8,False))
    return tests

if __name__ == "__main__":
    runTests()

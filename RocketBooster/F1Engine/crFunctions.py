"""All functions in this method must have take a single argument which is a comma
delimited string.  They must split the string if they take more than one argument 
and change them into the form it needs.

lock predictor data
reset predictor data
unlock predictor data
set update schedule (comic id, list of day/hour tuples)
"""

from J2Engine.cache import *

def resetPredData(argList):
    """Reset the predictor history to default settings.
    
    argList should be a comic id"""
    try:
        comicId = int(argList)
    except ValueError:
        return False
    #Do stuff to reset predictor history of comicId
    return False
    
def lockPredData(argList):
    """Lock a comics expected update schedule.
    
    argList should be a comic id
    Use this if a comic is going on hiatus and you want to avoid the predictor
    data losing accuracy."""
    try:
        comicId = int(argList)
    except ValueError:
        return False
    #Do stuff to lock the predictor data of comicId
    return False
    
def unlockPredData(argList):
    """Unlock a comics expected update schedule.
    
    argList should be a comic id"""
    try:
        comicId = int(argList)
    except ValueError:
        return False
    #Do stuff to unlock the predictor data of comicId
    return False
    
def setUpdateSchedule(argList):
    """Set a comics update schedule to provided times.
    
    argList should be a comicId and a list of (day,hour) tuples"""
    try:
        argList = argList.partition(',')
        comicId = int(argList[0])
        schedule = argList[2].strip('[]')
        schedule = schedule.split(',')
    except ValueError:
        return False
    #Update the predictor history using the provided list
    return False
    
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
    
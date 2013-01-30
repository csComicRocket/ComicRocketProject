"""All functions in this method must have take a single argument which is a comma
delimited string.  They must split the string if they take more than one argument 
and change them into the form it needs.

lock predictor data
reset predictor data
unlock predictor data
set update schedule (comic id, list of day/hour tuples)
"""

def resetPredData(argList):
    """Reset the predictor history to default settings.
    
    argList should be a comic id"""
    try:
        comicId = int(argList)
    except ValueError:
        return
    #Do stuff to reset predictor history of comicId
    
def lockPredData(argList):
    """Lock a comics expected update schedule.
    
    argList should be a comic id
    Use this if a comic is going on hiatus and you want to avoid the predictor
    data losing accuracy."""
    try:
        comicId = int(argList)
    except ValueError:
        return
    #Do stuff to lock the predictor data of comicId
    
def unlockPredData(argList):
    """Unlock a comics expected update schedule.
    
    argList should be a comic id"""
    try:
        comicId = int(argList)
    except ValueError:
        return
    #Do stuff to unlock the predictor data of comicId
    
def setUpdateSchedule(argList):
    """Set a comics update schedule to provided times.
    
    argList should be a comicId and a list of (day,hour) tuples"""
    try:
        argList = argList.partition(',')
        comicId = int(argList[0])
        schedule = argList[2] #still needs work
    except ValueError:
        return
    #Update the predictor history using the provided list
"""All functions in this method must have take a single argument which is a comma
delimited string.  They must split the string if they take more than one argument 
and change them into the form it needs."""

def resetPredHist(argList):
    """Reset the predictor history to default settings."""
    try:
        comicId = int(argList)
    except ValueError:
        return
    #Do stuff to reset predictor history of comicId
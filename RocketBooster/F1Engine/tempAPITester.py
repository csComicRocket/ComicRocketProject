import crFunctions

def callMethod(string):
    string = string.partition('(')
    funcName = string[0]
    args = string[2].rpartition(')')
    try:
        methodToCall = getattr(crFunctions, funcName)
    except AttributeError:
        return
    methodToCall(args[0])
    
if __name__ == '__main__':
    callMethod("resetPredHist(1101)")
    callMethod("resetPredHist(1,2,3)")
    callMethod("invalidName()")
    callMethod("invalidName2")
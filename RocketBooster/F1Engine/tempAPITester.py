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
    
def runTests():
    tests = []
    try:
        callMethod("resetPredData(1101)")
        tests.append(("callMethod",1,True))
    except:
        tests.append(("callMethod",1,False))
    try:
        callMethod("resetPredData(1,2,3)")
        tests.append(("callMethod",2,True))
    except:
        tests.append(("callMethod",2,False))
    try:
        callMethod("invalidName()")
        tests.append(("callMethod",3,True))
    except:
        tests.append(("callMethod",3,False))
    try:
        callMethod("invalidFormat")
        tests.append(("callMethod",4,True))
    except:
        tests.append(("callMethod",4,False))
    return tests
    
if __name__ == '__main__':
    runTests()
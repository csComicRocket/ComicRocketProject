import crFunctions

def callMethod(string):
    string = string.partition('(')
    funcName = string[0]
    args = string[2].rpartition(')')
    try:
        methodToCall = getattr(crFunctions, funcName)
    except AttributeError:
        return False
    methodToCall(args[0])
    
def runTests():
    tests = []
    try
        tests.append(("callMethod",1,callMethod("resetPredData(1101)")))
    except:
        tests.append(("callMethod",1,False))
    try:
        tests.append(("callMethod",2, not callMethod("resetPredData(1,2,3)")))
    except:
        tests.append(("callMethod",2,False))
    try:
        tests.append(("callMethod",3,not callMethod("invalidName()")))
    except:
        tests.append(("callMethod",3,False))
    try:
        tests.append(("callMethod",4,not callMethod("()invalidFormat")))
    except:
        tests.append(("callMethod",4,False))
    try:
        crFunctionsTests = callMethod("runTests()")
        tests.append(("callMethod",5,True))
    except:
        tests..append(("callMethod",5,False))
    return tests
    
if __name__ == '__main__':
    runTests()
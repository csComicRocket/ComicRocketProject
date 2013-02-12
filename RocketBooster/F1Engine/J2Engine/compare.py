#Eric Smith
from LunarModule.pageTree import *
#takes 2 pageTree objects and compares thier hash values, True if they are the same, False if they are different
def compare(hashObj1,hashObj2):
    if(hashObj1.getHash() == hashObj2.getHash()):
        return True
    else:
        return False

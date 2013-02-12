#Eric Smith
from pageTree import *

def hashPageTree(pageTreeObj):
    """Hashes a object stores it"""
    pageTree.setHash(0,hash(pageTreeObj.getContent(0)))
    return None

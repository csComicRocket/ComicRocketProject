# Code for pageTree, pageNode, and sanitizeId function originated from
# Brett Alistair Kromkamp - brettkromkamp@gmail.com
# www.quesucede.com
# Code has been modified. Class, variable, and function names have been
# changed from Brett's original code. Data types have been changed and
# new data members and corresponding methods [will be] added to code.
# Tree structure is kept from original code. [might be changed, but doubt it.]

import uuid

from utilities import sanitizeId
from pageNode import PageNode

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

"""Class PageTree holds a root page (the one we're pulling, comparing, etc) plus its children (css etc)."""
class PageTree:

    """PageTree.__init__(url) creates root node with given url"""
    def __init__(self, url=None):
        self.nodes = []
        if url is not None:
            self.createPageNode(url, 0)

    """PageTree.getIndex(position) returns the index of the node at nodeId=position."""
    def getIndex(self, position):
        for index, node in enumerate(self.nodes):
            if node.nodeId == position:
                break
        return index

    """PageTree.createPageNode(url:string, nodeId:integer, parent:integer=None)

       If parent is not given, it is the root of the pageTree. Conventionally, give root an id of 0.
       Otherwise specify parent's identification, for example a css file might have 0 as its parent.
       Conventionally, give child elements incrementing id numbers, 1..n."""
    def createPageNode(self, url, nodeId=None, parent=None, sourceMode=None\
content=None, encodeType=None, pullTS=None):

        node = PageNode(url, nodeId, sourceMode, content, encodeType, pullTS)
        self.nodes.append(node)
        self.__updateFPointer(parent, node.nodeId, _ADD)
        node.bPointer = parent
        return node

    """PageTree.show(position, level=_ROOT) prints the pageTree depth first kinda like this:

       http://www.rooturl.com [0]
       ('/t', 'http://www.rooturl.com/child [1]')
       ('/t/t', 'http://www.rooturl.com/child/child [2]')
       etc."""
    def show(self, position, level=_ROOT):
        queue = self[position].fPointer
        if level == _ROOT:
            print("{0} [{1}]".format(self[position].url,
                                     self[position].nodeId))
        else:
            print("\t"*level, "{0} [{1}]".format(self[position].url,
                                                 self[position].nodeId))
        if self[position].expanded:
            level += 1
            for element in queue:
                self.show(element, level)  # recursive call


    """PageTree.expandPageTree(position, mode=_DEPTH) prints id's separated by new lines, _DEPTH or _WIDTH first"""
    def expandPageTree(self, position, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 'Essential LISP' by
        # John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        yield position
        queue = self[position].fPointer
        while queue:
            yield queue[0]
            expansion = self[queue[0]].fPointer
            if mode is _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode is _WIDTH:
                queue = queue[1:] + expansion  # width-first

    """PageTree.isBranch(position) returns the list of children of the current pageTree id=position."""
    def isBranch(self, position):
        return self[position].fPointer

    """PageTree.__updateFPointer(position, nodeId, mode) :: Don't touch."""
    def __updateFPointer(self, position, nodeId, mode):
        if position is None:
            return
        else:
            self[position].updateFPointer(nodeId, mode)

    """PageTree.__updateBPointer(position, nodeId) :: Don't touch."""
    def __updateBPointer(self, position, nodeId):
        self[position].bPointer = nodeId

    """PageTree.__getitem__(key) I think this is a Python object utility function. Returns index of key."""
    def __getitem__(self, key):
        return self.nodes[self.getIndex(key)]

    """PageTree.__setitem__(key) I think this is a Python object utility function. Sets index of key."""
    def __setitem__(self, key, item):
        self.nodes[self.getIndex(key)] = item

    """PageTree.__len__() I think this is a Python object utility function. Returns len(self.nodes)."""
    def __len__(self):
        return len(self.nodes)


    """PageTree.__contains__(nodeId) I think this is a Python object utility function. Returns id?"""
    def __contains__(self, nodeId):
        return [node.nodeId for node in self.nodes
                if node.nodeId is nodeId]

    """PageTree.setContent(nodeId, content, encodeType) sets both content and encodeType, believe it or not."""
    def setContent(self, nodeId, content, encodeType):
        self.nodes[self.getIndex(nodeId)].setContent(content, encodeType)

    """PageTree.getContent(nodeId) returns content of tree node nodeId."""
    def getContent(self, nodeId):
        return self.nodes[self.getIndex(nodeId)].getContent()

    """PageTree.setUrl(nodeId, url) changes the url of the node nodeId."""
    def setUrl(self, nodeId, url):
        self.nodes[self.getIndex(nodeId)].setUrl(url)
    """PageTree.getUrl(nodeId) returns the url of node nodeId."""
    def getUrl(self, nodeId):
        return self.nodes[self.getIndex(nodeId)].getUrl()

    """PageTree.setElementId(nodeId, elementId) sets the elementId of node nodeId."""
    def setElementId(self, nodeId, elementId):
        self.nodes[self.getIndex(nodeId)].setElementId(elementId)
    """PageTree.getElementId(nodeId) returns the elementId of node nodeId."""
    def getElementId(self, nodeId):
        return self.nodes[self.getIndex(nodeId)].getElementId()

    """PageTree.setSourceMode(nodeId, sourceMode) changes the sourceMode of node nodeId."""
    def setSourceMode(self, nodeId, sourceMode):
        self.nodes[self.getIndex(nodeId)].setSourceMode(sourceMode)
    """PageTree.getSourceMode(nodeId) returns the sourceMode of node nodeId."""
    def getSourceMode(self, nodeId):
        return self.nodes[self.getIndex(nodeId)].getSourceMode()

    """PageTree.setEncodeType(nodeId, encodeType) sets the encodeType of node nodeId."""
    def setEncodeType(self, nodeId, encodeType):
        self.nodes[self.getIndex(nodeId)].setEncodeType(encodeType)
    """PageTree.getEncodeType(nodeId) returns the encodeType of node nodeId."""
    def getEncodeType(self, nodeId):
        return self.nodes[self.getIndex(nodeId)].getEncodeType()

    """PageTree.setMimeType(nodeId, mimeType) sets the mimeType of node nodeId."""
    def setMimeType(self, nodeId, mimeType):
        self.nodes[self.getIndex(nodeId)].setMimeType(mimeType)
    """PageTree.getMimeType(nodeId) returns the mimeType of node nodeId."""
    def getMimeType(self, nodeId):
        return self.nodes[self.getIndex(nodeId)].getMimeType()

    """PageTree.setAuthorTS(nodeId, authorTS) sets the authorTimeStamp. AuthorTimeStamp should not be a list."""
    def setAuthorTS(self, nodeId, authorTS):
        self.nodes[self.getIndex(nodeId)].setAuthorTS(authorTS)

    """PageTree.getAuthorTS(nodeId) gets the authorTimeStamp from node nodeId."""
    def getAuthorTS(self, nodeId):
        return self.nodes[self.getIndex(nodeId)].getAuthorTS()

    """PageTree.setPullTS(nodeId, pullTS) sets the pullTimeStamp.

    PullTS could be either an individual timestamp or a list of timestamps."""
    def setPullTS(self, nodeId, pullTS):
        self.nodes[self.getIndex(nodeId)].setPullTS(pullTS)

    """PageTree.clearPullTS(nodeId) empties the timestamp list of node nodeId."""
    def clearPullTS(self, nodeId):
        self.nodes[self.getIndex(nodeId)].clearPullTS()

    """PageTree.getPullTS(nodeId) returns list of pullTimeStamps of node nodeId."""
    def getPullTS(self, nodeId):
        self.nodes[self.getIndex(nodeId)].getPullTS()

    """PageTree.setRevisionNum(nodeId, revisionNum) sets the revisionNum of node nodeId."""
    def setRevisionNum(self, nodeId, revisionNum):
        self.nodes[self.getIndex(nodeId)].setRevisionNum(revisionNum)
    """PageTree.getRevisionNum(nodeId) returns the revisionNum of node nodeId."""
    def getRevisionNum(self, nodeId):
        return self.nodes[self.getIndex(nodeId)].getRevisionNum()

    """PageTree.isReferredTo(nodeId) increments the isReferredTo member of node nodeId."""
    def isReferredTo(self, nodeId):
        self.nodes[self.getIndex(nodeId)].isReferredTo()

"""PageTree's main function: currently builds a little pageTree with 10 nodes sorta randomly connected, then prints."""
if __name__== "__main__":

    pageTree = PageTree(None)
    pageTree.createPageNode("http://www.xkcd.com", 0)  # root node
    pageTree.createPageNode("http://www.xkcd.com/apic.jpg", 1, parent = 0)
    pageTree.createPageNode("http://www.xkcd.com/style.css", 2, parent = 0)
    pageTree.createPageNode("Joe", 3, parent = 1)
    pageTree.createPageNode("Diane", 4, parent = 2)
    pageTree.createPageNode("George", 5, parent = 4)
    pageTree.createPageNode("Mary", 6, parent = 2)
    pageTree.createPageNode("Jill", 7, parent = 5)
    pageTree.createPageNode("Carol", 8, parent = 7)
    pageTree.createPageNode("Grace", 9, parent = 2)
    pageTree.createPageNode("Mark", 10, parent = 1)

    print("="*80)
    pageTree.show(0)
    print("="*80)
    for node in pageTree.expandPageTree(0, mode=_WIDTH):
        print(node)
    print("="*80)

    print(">> Example of setting and getting content")
    content = "Stuff"
    encodeType = "text"
    pageTree.setContent(0, content, encodeType)
    print(pageTree.getContent(0))

    print(">> Example of getting and setting authorTimeStamp and pullTimeStamp")
    authorTS = "Nov 30, 2012"
    pageTree.setAuthorTS(0, authorTS)
    print("Author TS: " + pageTree.getAuthorTS(0))
    pullTSOriginal = "Nov 27, 2012"
    pullTSNew = "Dec 2, 2012"
    pageTree.setPullTS(0, pullTSOriginal)
    pageTree.setPullTS(0, pullTSNew)
    print("Pull TS: ")
    print(pageTree.getPullTS(0))
    pageTree.clearPullTS(0)
    pullTSList = [pullTSOriginal, pullTSNew]
    pageTree.setPullTS(0, pullTSList)
    print("Pull TS: ")
    print(pageTree.getPullTS(0))
    print("It's evident that it doesn't work at the moment. TODO: fix it.")

    print(">> Example of something else.")

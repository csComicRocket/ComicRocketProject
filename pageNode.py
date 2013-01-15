# Code for pageTree, pageNode, and sanitizeId function originated from
# Brett Alistair Kromkamp - brettkromkamp@gmail.com
# www.quesucede.com
# Code has been modified. Class, variable, and function names have been
# changed from Brett's original code. Data types have been changed and
# new data members and corresponding methods [will be] added to code.
# Tree structure is kept from original code. [might be changed, but doubt it.]

import uuid

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

"""Class PageNode: Defines pageNodes of a tree.

Each pageNode contains a url, an nodeId, a pointer to the parent, and a list of pointers to its children.
PageNode will contain more data than that later on, and each data will have a corresponding get/set function.
(OR I will encapsulate the data and force you to have tree.pageNode.item.data.value Buuuhahahahahaha)"""
class PageNode:

    """PageNode.__init__(url, nodeId, sourceMode, content, encodeType, pullTS, expanded=True):

    Sets corresponding data for pageNode.
    Note __bPointer is set to None initially, then is reset later.
    Note __fPointer is set to an empty list.
    url and nodeId are required."""
    def __init__(self, url, nodeId, sourceMode=None,\
 content=None, encodeType=None, pullTS=None, expanded=True):
        self.__nodeId = (uuid.uuid1() if nodeId is None else
                nodeId)
        self.url = url
        self.sourceMode = sourceMode
        self.expanded = expanded
        self.__bPointer = None
        self.__fPointer = []
        self.content = content
        self.comicId = None
        self.encodeType = encodeType
        self.mimeType = None
        self.authorTimeStamp = None
        self.pullTimeStamp = []
        self.revisionNum = None
        self.revisionHistory = None
        self.isReferredTo = 1 # because there's obviously at least one tree pointing to this node.
        self.hash = None
        try:
            self.pullTimeStamp.extend(pullTS)
        except:
            self.pullTimeStamp.append(pullTS if pullTS is not None else None)

    """PageNode.nodeId() returns id of pageNode. Root should be 0."""
    @property
    def nodeId(self):
        return self.__nodeId

    """PageNode.bPointer() returns __bPointer"""
    @property
    def bPointer(self):
        return self.__bPointer

    """PageNode.bPointer(value) sets __bPointer = value"""
    @bPointer.setter
    def bPointer(self, value):
        if value is not None:
            self.__bPointer = value

    """PageNode.fPointer() returns __fPointer (list)"""
    @property
    def fPointer(self):
        return self.__fPointer

    """PageNode.updateFPointer(ideentifier, mode=_ADD):

    Appends an nodeId to the list of children if mode is _ADD.
    Removes id from list of children if mode is _DELETE.
    Sets entire list = [nodeId] if mode is _INSERT."""
    def updateFPointer(self, nodeId, mode=_ADD):
        if mode is _ADD:
            self.__fPointer.append(nodeId)
        elif mode is _DELETE:
            self.__fPointer.remove(nodeId)
        elif mode is _INSERT:
            self.__fPointer = [nodeId]

    """PageNode.setContent(content, encodeType) sets both content and encodeType."""
    def setContent(self, content, encodeType):
        self.content = content
        self.encodeType = encodeType

    """PageNode.getContent() returns only content."""
    def getContent(self):
        return self.content

    """PageNode.getEncodeType() returns only encodeType."""
    def getEncodeType(self):
        return self.encodeType
    
    """PageNode.setUrl(url) sets the url."""
    def setUrl(self, url):
        self.url = url
    """PageNode.getUrl() returns the url."""
    def getUrl(self):
        return self.url

    """PageNode.setComicId(comicId) sets the comicId."""
    def setComicId(self, comicId):
        self.comicId = comicId
    """PageNode.getComicId() returns the comicId."""
    def getComicId(self):
        return self.comicId

    """PageNode.setSourceMode(sourceMode) sets the sourceMode."""
    def setSourceMode(self, sourceMode):
        self.sourceMode = sourceMode
    """PageNode.getSourceMode() returns the sourceMode."""
    def getSourceMode(self):
        return self.sourceMode

    """PageNode.setEncodeType(encodeType) sets the encodeType."""
    def setEncodeType(self, encodeType):
        self.encodeType = encodeType
    """PageNode.getEncodeType() returns the encodeType."""
    def getEncodeType(self):
        return self.encodeType

    """PageNode.setMimeType(mimeType) sets the mimeType."""
    def setMimeType(self, mimeType):
        self.mimeType = mimeType
    """PageNode.getMimeType() returns the mimeType."""
    def getMimeType(self):
        return self.mimeType

    """PageNode.setAuthorTS(authorTS) sets the authorTimeStamp. AuthorTimeStamp should not be a list."""
    def setAuthorTS(self, authorTS):
        self.authorTimeStamp = authorTS

    """PageNode.getAuthorTS(nodeId) gets the authorTimeStamp."""
    def getAuthorTS(self):
        return self.authorTimeStamp

    """PageNode.setPullTS(pullTS) sets the pullTimeStamp.

    PullTS could be either an individual timestamp or a list of timestamps."""
    def setPullTS(self, pullTS):
        print pullTS
        if self.pullTimeStamp is None:
            self.pullTimeStamp = []
        try:
            print("trying to extend pullTS with a list")
            self.pullTimeStamp.append(pullTS)
        except:
            print("...failed..")
            self.pullTimeStamp.append(pullTS)

    """PageNode.clearPullTS() empties the pullTimeStamp list."""
    def clearPullTS(self):
        del self.pullTimeStamp[:]

    """PageNode.getPullTS(nodeId) returns list of pullTimeStamps."""
    def getPullTS(self):
        return self.pullTimeStamp

    """PageNode.setRevisionNum(revisionNum) sets the revisionNum."""
    def setRevisionNum(self, revisionNum):
        self.revisionNum = revisionNum
    """PageNode.getRevisionNum() returns the revisionNum."""
    def getRevisionNum(self):
        return self.revisionNum

    """PageNode.isReferredTo() increments the isReferredTo member."""
    def isReferredTo(self):
        self.isReferredTo =+1

    """PageNode.setHash(hash) sets the hash."""
    def setHash(self, hash):
        self.hash = hash
    """PageNode.getHash() returns the hash."""
    def getHash(self):
        return self.hash

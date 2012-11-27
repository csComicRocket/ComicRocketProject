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

Each pageNode contains a url, an identifier, a pointer to the parent, and a list of pointers to its children.
PageNode will contain more data than that later on, and each data will have a corresponding get/set function.
(OR I will encapsulate the data and force you to have tree.pageNode.item.data.value Buuuhahahahahaha)"""
class PageNode:

    """PageNode.__init__(url:string, identifier:integer=None, expanded:booleanish=True):

    Sets corresponding data for pageNode.
    Note __bPointer is set to None initially, then is reset later.
    Note __fPointer is set to an empty list."""
    def __init__(self, url="George", identifier=None, expanded=True):
        self.__identifier = (uuid.uuid1() if identifier is None else
                identifier)
        self.url = url
        self.expanded = expanded
        self.__bPointer = None
        self.__fPointer = []

    """PageNode.identifier() returns id of pageNode. Root should be 0."""
    @property
    def identifier(self):
        return self.__identifier

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

    Appends an identifier to the list of children if mode is _ADD.
    Removes id from list of children if mode is _DELETE.
    Sets entire list = [identifier] if mode is _INSERT."""
    def updateFPointer(self, identifier, mode=_ADD):
        if mode is _ADD:
            self.__fPointer.append(identifier)
        elif mode is _DELETE:
            self.__fPointer.remove(identifier)
        elif mode is _INSERT:
            self.__fPointer = [identifier]


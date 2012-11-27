import uuid

from utilities import sanitizeId
from pageNode import PageNode

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

"""Class PageTree holds a root page (the one we're pulling, comparing, etc) plus its children (css etc)."""
class PageTree:

    """PageTree.__init__() doesn't do much by itself"""
    def __init__(self):
        self.nodes = []

    """PageTree.getIndex(position) returns the index of the node at identifier=position."""
    def getIndex(self, position):
        for index, node in enumerate(self.nodes):
            if node.identifier == position:
                break
        return index

    """PageTree.createPageNode(url:string, identifier:integer, parent:integer=None)

       If parent is not given, it is the root of the pageTree. Conventionally, give root an id of 0.
       Otherwise specify parent's identification, for example a css file might have 0 as its parent.
       Conventionally, give child elements incrementing id numbers, 1..n."""
    def createPageNode(self, url, identifier=None, parent=None):

        node = PageNode(url, identifier)
        self.nodes.append(node)
        self.__updateFPointer(parent, node.identifier, _ADD)
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
                                     self[position].identifier))
        else:
            print("\t"*level, "{0} [{1}]".format(self[position].url,
                                                 self[position].identifier))
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

    """PageTree.__updateFPointer(position, identifier, mode) :: Don't touch."""
    def __updateFPointer(self, position, identifier, mode):
        if position is None:
            return
        else:
            self[position].updateFPointer(identifier, mode)

    """PageTree.__updateBPointer(position, identifier) :: Don't touch."""
    def __updateBPointer(self, position, identifier):
        self[position].bPointer = identifier

    """PageTree.__getitem__(key) I think this is a Python object utility function. Returns index of key."""
    def __getitem__(self, key):
        return self.nodes[self.getIndex(key)]

    """PageTree.__setitem__(key) I think this is a Python object utility function. Sets index of key."""
    def __setitem__(self, key, item):
        self.nodes[self.getIndex(key)] = item

    """PageTree.__len__() I think this is a Python object utility function. Returns len(self.nodes)."""
    def __len__(self):
        return len(self.nodes)


    """PageTree.__contains__(identifier) I think this is a Python object utility function. Returns id?"""
    def __contains__(self, identifier):
        return [node.identifier for node in self.nodes
                if node.identifier is identifier]

"""PageTree's main function: currently builds a little pageTree with 10 nodes sorta randomly connected, then prints."""
if __name__== "__main__":

    pageTree = PageTree()
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


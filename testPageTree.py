
import uuid

from utilities import sanitizeId
from pageNode import PageNode
from pageTree import PageTree

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

class TestPageTree:
    def testInit(self):
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
        return pageTree

    def testInit2(self):
        pageTree = PageTree("http://testingInit2/")
        pageTree.createPageNode("http://www.xkcd.com/apic.jpg", 1, parent = 0)
        pageTree.createPageNode("http://www.xkcd.com/style.css", 2, parent = 0)
        return pageTree
    
    def printTree(self, pageTree):
        print("="*80)
        pageTree.show(0)
        print("="*80)
        for node in pageTree.expandPageTree(0, mode=_WIDTH):
            print(node)
        

if __name__ == '__main__':
    t = TestPageTree()
    
    pageTree = t.testInit()
    t.printTree(pageTree)
    pageTree = t.testInit2()
    t.printTree(pageTree)

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

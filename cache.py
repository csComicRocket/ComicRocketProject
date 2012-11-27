
from pageTree import PageTree
from pageNode import PageNode

class Cache:

    def __init__(self):
        print("Hi, I'm a new Cache")

    def storeCache(self, pageTree):
        print("storeCache says, here is your new pageTree:")
        pageTree.show(0)

    def fetchCache(self, url, needsChildren):
        print("fetchCache is now building trees (cause I don't have a cache to pull from yet :)")
        # Populate a pageTree with data from my awesome cache.
        # If needsChildren = true, will pull whole pageTree.
        # API for cache to pull data tba.
        pageTree = PageTree()
        pageTree.createPageNode(url, 0)
        if needsChildren:
            pageTree.createPageNode("http://www.dummyurl.com/child", 1, parent=0)
            pageTree.createPageNode("http://www.dummyurl.com/child/child", 2, parent=1)
            pageTree.createPageNode("http://www.dummyurl.com/child", 3, parent=1)
            pageTree.createPageNode("http://www.dummyurl.com/child", 4, parent=3)
            pageTree.createPageNode("http://www.dummyurl.com/child", 5, parent=4)
            pageTree.createPageNode("http://www.dummyurl.com/child", 6, parent=5)
            pageTree.createPageNode("http://www.dummyurl.com/child", 7, parent=2)
            pageTree.createPageNode("http://www.dummyurl.com/child", 8, parent=3)
            pageTree.createPageNode("http://www.dummyurl.com/child", 9, parent=7)
            pageTree.createPageNode("http://www.dummyurl.com/child", 10, parent=4)
        return pageTree

    def testCache(self):
        aTreeOnlyRoot = self.fetchCache("http://www.dummyurl.com/", 0)
        self.storeCache(aTreeOnlyRoot)
        print("\n")
        aTreeWithChildren = self.fetchCache("http://www.dummyurl.com/", "I would like page's children, please")
        self.storeCache(aTreeWithChildren)

if __name__ == '__main__':
    cache = Cache()

    cache.testCache()


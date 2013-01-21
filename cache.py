import os
import shutil

from pageTree import PageTree
from pageNode import PageNode

class Cache:

    def __init__(self):
        print("Hi, I'm a new Cache")

    def storeCache(self, pageTree):
        print("storeCache says, here is your new pageTree:")
        pageTree.show(0)
        temp = self.parseDirectory(pageTree.getUrl(0))
        dir = temp[0]
        fName = temp[1]
        try:
            os.makedirs(dir)
        except OSError:
            pass #if an error is thrown it means the directory already exists
        try:
            with open(os.path.join(dir, fName)) as f:
                pass  #non race way to check to see if the file already exists
            self.revisionPush(pageTree, dir, fName)
        except IOError: #if an error occurs the file does not yet exist, which means this is a new page
            self.storeInLast3(pageTree.getComicId(0), pageTree.getUrl(0))
        with open(os.path.join(dir,"pageTreeData.txt"), 'w+') as f:
            f.writelines(pageTree.getPageTreeData())
        with open(os.path.join(dir, fName), 'w+') as f:
            f.write(str(pageTree.getContent(0)))
        
    def parseDirectory(self, url):
        """Split a url and make it into a directory name."""
        dir = url.split("//")
        dir = dir[1].rpartition('/')
        if dir[2] == "":
            dir = dir[0].rpartition('/')
        if dir[0] == "":
            return dir[2], "default"
        return dir[0], dir[2]
        
    def revisionPush(self, pageTree, dir, fName):
        rNum = self.findRevisionNum(dir, fName)
        newFName = str(rNum) + '_' + fName
        os.rename(os.path.join(dir, fName), os.path.join(dir, newFName))
        os.rename(os.path.join(dir, "pageTreeData.txt"), os.path.join(dir, str(rNum) + '_' + "pageTreeData.txt"))
        #do something to set the revision number of the current pageTree to rNum+1
        print "I am not finished"
    
    def findRevisionNum(self, dir, fName):
        rNum = 0
        while (True):
            try:
                with open(os.path.join(dir, str(rNum) + '_' + fName)) as f:
                    pass
                rNum += 1
            except IOError:
                return rNum

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
        aTreeWithChildren = self.fetchCache("http://www.dummyurl.com/bleh.html", "I would like page's children, please")
        self.storeCache(aTreeWithChildren)
        self.storeCache(aTreeWithChildren)
        self.storeInLast3(101, 'http://www.aurl.com')
        self.storeInLast3(101, 'http://www.anotherurl.com')
        self.storeInLast3(101, 'http://www.anothernotherurl.com')
        self.storeInLast3(101, 'http://www.anothernothernothernothernotherurl.com')
        aUrl = "http://www.dummyurl.com/child/child/img.jpg"
        print aUrl, "->", self.parseDirectory(aUrl)
        anotherUrl = "http://www.dummyurl.com/child/child/"
        print anotherUrl, "->", self.parseDirectory(anotherUrl)
        anotherUrl = "http://www.dummyurl.com/"
        print anotherUrl, "->", self.parseDirectory(anotherUrl)
        anotherUrl = "http://www.dummyurl.com"
        print anotherUrl, "->", self.parseDirectory(anotherUrl)
		
    def storeInLast3(self, comicId, url):
        """Adds the data from the given pageTree object to the list of last 3 urls.
        
        This function should only be called when the pageTree object does not have
        a current version in the cache."""
        dir = "predictorInfo/" + str(comicId) + "/"
        try:
            os.makedirs(dir)
            shutil.copy2("predictorInfo/predictorData.txt", dir)
        except OSError:
            pass #if an error is thrown it means the directory already exists
        try:
            with open(dir + "last3Pages.txt") as f:
                urlList = f.readlines()
        except IOError: #if an error occurs the file does not yet exist
            urlList = []
        if len(urlList) >= 3:
            urlList.pop(0)
        urlList.append(url + '\n')
        with open(dir + "last3Pages.txt", 'w+') as f:
            f.writelines(urlList)
		
if __name__ == '__main__':
    cache = Cache()

    cache.testCache()


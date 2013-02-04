import os
import shutil
import time

from LunarModule.pageTree import PageTree
from LunarModule.pageNode import PageNode

class Cache:

    def __init__(self):
        print("Hi, I'm a new Cache")

    def storeCache(self, pageTree):
        print("storeCache says, here is your new pageTree:")
        pageTree.show(0)
        temp = self.parseDirectory(pageTree.getUrl(0))
        directory = temp[0]
        fName = temp[1]
        try:
            os.makedirs(directory)
        except OSError:
            pass #if an error is thrown it means the directory already exists
        try:
            with open(os.path.join(directory, fName)) as f:
                pass  #non race way to check to see if the file already exists
            self.revisionPush(pageTree, directory, fName)
        except IOError: #if an error occurs the file does not yet exist, which means this is a new page
            self.storeInLast3(pageTree.getComicId(0), pageTree.getUrl(0))
            self.storeInHistoryList(directory, pageTree.getUrl(0))
        with open(os.path.join(directory,"pageTreeData.txt"), 'w+') as f:
            f.writelines(pageTree.getPageTreeData())
        with open(os.path.join(directory, fName), 'w+') as f:
            f.write(str(pageTree.getContent(0)))
        
    def parseDirectory(self, url):
        """Split a url and make it into a directory name."""
        if url.endswith("//"):
            return "../../cache/cacheInfo/default/", "default"
        if "//" in url:
            directory = url.split("//")[1]
        directory = directory.rpartition('/')
        if directory[2] == "":
            directory = directory[0].rpartition('/')
        if directory[0] == "":
            return "../../cache/cacheInfo/" + directory[2], "default"
        return "../../cache/cacheInfo/" + directory[0], directory[2]
        
    def revisionPush(self, pageTree, directory, fName):
        rNum = self.findRevisionNum(directory, fName)
        pageTree.setRevisionNum(0, rNum+1)
        newFName = str(rNum) + '_' + fName
        os.rename(os.path.join(directory, fName), os.path.join(directory, newFName))
        os.rename(os.path.join(directory, "pageTreeData.txt"), os.path.join(directory, str(rNum) + '_' + "pageTreeData.txt"))
        #do something to set the revision number of the current pageTree to rNum+1
        # Already done. See above "pageTree.setRevisionNum(0, rNum+1)"
        print "I am not finished"
    
    def findRevisionNum(self, directory, fName):
        fName = "pageTreeData.txt" #Please!!!!! Remember to take this out maybe someday.
        print os.path.join(directory, fName)
        rNum = 0
        try:
            with open(os.path.join(directory, fName)) as f:
                fileString = f.read()
                print "file: ", fileString
                print "file after split at RevisionNum: ", fileString.split("RevisionNum: ")[1].split("\n")[0]
                rNumString = fileString.split("RevisionNum: ")[1].split("\n")[0]
                if rNumString == "None":
                    rNum = 0
                else:
                    rNum = int(rNumString)
                print "rNum: ", rNum
                return rNum
        except IOError:
            return rNum
        except IndexError:
            return rNum

    def updateTimeStamp(self, pageTree):
        fName = parseDirectory(pageTree.getUrl(0))

        newFileString = "" # to put it in right scope... maybe??

        try:
            with open(os.path.join(directory, fName)) as f:
                fileString = f.read()
                print "file: ", fileString
                timeStampString = fileString.split("TimeStamp: ")[1].split("\n")[0]
                newFileString = fileString.split("TimeStamp: ")[1] + "TimeStamp: " + timeStampString + pageTree.getPullTS(0) + "\n" + fileString.split("TimeStamp: ")[1].split("\n")[1] #Dumb
            with open(os.path.join(directory, fName), 'w+') as f:
                f.writelines(newFileString)
        except IOError:
            print "IO error updating timestamp. pageTree:" + pageTree
        except IndexError:
            print "Index error updating timestamp. pageTree:" + pageTree

    def storeInLast3(self, comicId, url):
        """Adds the data from the given pageTree object to the list of last 3 urls.
        
        This function should only be called when the pageTree object does not have
        a current version in the cache."""
        directory = "../../cache/predictorInfo/" + str(comicId) + "/"
        try:
            os.makedirs(directory)
            defaultPredData(comicId)
        except OSError:
            pass #if an error is thrown it means the directory already exists
        try:
            with open(directory + "last3Pages.txt") as f:
                urlList = f.readlines()
        except IOError: #if an error occurs the file does not yet exist
            urlList = []
        if len(urlList) >= 3:
            urlList.pop(0)
        urlList.append(url + '\n')
        with open(directory + "last3Pages.txt", 'w+') as f:
            f.writelines(urlList)
            
    def storeInHistoryList(self, directory, url):
        temp = directory.split('/')
        directory = temp[0] + '/' + temp[1] + '/' + temp[2] + '/' + temp[3] + '/' + temp[4] + '/' 
        try:
            with open(os.path.join(directory, "historyData.txt")) as f:
                pass
        except IOError:
            with open(os.path.join(directory, "historyData.txt"), 'a+') as f:
                f.write(time.strftime(time.gmtime(), gmtime()) + '\n')
                f.write('0/n')
        with open(os.path.join(directory, "historyList.txt"), 'a+') as f:
                f.write(url + '\n')

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

    def testRootOnlyTreeWrite(self):
        aTreeOnlyRoot = self.fetchCache("http://www.dummyurl.com/", 0)
        self.storeCache(aTreeOnlyRoot)

    def testSpecificNameTree(self, treeRootDir):
        pageTree = PageTree()
        pageTree.createPageNode(treeRootDir, 0)
        self.storeCache(pageTree)

    def testMalformedUrl(self):
        url = "some.really.bad./wrongurl//"
        pageTree = PageTree()
        pageTree.createPageNode(url, 0)
        self.storeCache(pageTree)

    def testUpdateTimeStamp(self):
        print "Testing updateTimeStamp()"
        pageTree = PageTree()
        pageTree.createPageNode("http://www.dummyurl.com/timeStampTest.html", 0)
        pageTree.setPullTS(0, "52")
        self.storeCache(pageTree)
        print "Stored original pageTree"
        pageTree.setPullTS(0, "53+1/2")
        print "Updating time stamp"
        self.updateTimeStamp(pageTree)

def defaultPredData(self, comicId):
    directory = "../../cache/predictorInfo/" + str(comicId) + "/"
    shutil.copy2("predictorInfo/predictorData.txt", directory)
        
if __name__ == '__main__':
    cache = Cache()

    cache.testCache()

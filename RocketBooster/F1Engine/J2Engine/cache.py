import os
import shutil
import time

from LunarModule.pageTree import PageTree
from LunarModule.pageNode import PageNode
from ...Predictor import Predictor

class Cache:

    def storeCache(self, pageTree):
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
            #Predictor.update((time.gmtime().tm_wday, time.gmtime().tm_hour), pageTree.getComicId(0))
        with open(os.path.join(directory,"pageTreeData.txt"), 'w+') as f:
            f.writelines(pageTree.getPageTreeData())
        with open(os.path.join(directory, fName), 'w+') as f:
            f.write(str(pageTree.getContent(0)))
        
    def parseDirectory(self, url):
        #Split a url and make it into a directory name.
        if url.endswith("//"):
            return "../../cache/cacheInfo/default/", "default"
        if "//" in url:
            directory = url.split("//")[1]
        directory = directory.rpartition('/')
        if directory[2] == "":
            directory = directory[0].rpartition('/')
        if directory[0] == "":
            return "../../cache/cacheInfo/" + directory[2] + "/default", "default"
        return "../../cache/cacheInfo/" + directory[0] + "/" + directory[2], directory[2]
        
    def revisionPush(self, pageTree, directory, fName):
        rNum = self.findRevisionNum(directory, fName)
        newFName = str(rNum) + '_' + fName
        os.rename(os.path.join(directory, fName), os.path.join(directory, newFName))
        os.rename(os.path.join(directory, "pageTreeData.txt"), os.path.join(directory, str(rNum) + '_' + "pageTreeData.txt"))
        pageTree.setRevisionNum(0, rNum+1)
    
    def findRevisionNum(self, directory, fName):
        fName = "pageTreeData.txt" #Please!!!!! Remember to take this out maybe someday.
        rNum = 0
        try:
            with open(os.path.join(directory, fName)) as f:
                fileString = f.read()
                rNumString = fileString.split("RevisionNum: ")[1].split("\n")[0]
                if rNumString == "None":
                    rNum = 0
                else:
                    rNum = int(rNumString)
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
            Predictor.scanDirectory(comicId)
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
        """Store the newly found url in the list of urls to be checked."""
        temp = directory.split('/')
        directory = temp[0] + '/' + temp[1] + '/' + temp[2] + '/' + temp[3] + '/' + temp[4] + '/' 
        try:
            with open(os.path.join(directory, "historyData.txt")) as f:
                pass
        except IOError:
            with open(os.path.join(directory, "historyData.txt"), 'a+') as f:
                f.write(time.strftime("%m", time.gmtime()) + '\n')
                f.write('0/n')
        with open(os.path.join(directory, "historyList.txt"), 'a+') as f:
            f.write(url + '\n')
        
    def fetchCache(self, url, versionNum = None):
        # Populate a pageTree with data from my awesome cache.
        # If needsChildren = true, will pull whole pageTree.
        # API for cache to pull data tba.
        directory = self.parseDirectory(url)
        fName = directory[1]
        directory = directory[0]

        preFileString = ""
        currVersionNum = self.findRevisionNum(directory, fName)
        if versionNum:
            if versionNum < 0:
                versionNum = currVersionNum + versionNum
            preFileString = versionNum + "_"
            if versionNum < 0 or versionNum > currVersionNum:
                preFileString = ""

        pageTree = PageTree(url)
        contentType = "Text"
        try:
            with open(os.path.join(directory, preFileString + "pageTreeData.txt")) as f:
                pageTree.setPageTreeData(f.read())
                contentType = pageTree.getEncodeType(0)
                pageTree.setSourceMode(0, "cache")
        except IOError:
            pass
        try:
            with open(os.path.join(directory, preFileString + fName)) as f:
                pageTree.setContent(0, f.read(), contentType)
        except IOError:
            pass
        return pageTree

    def clearPage(self, url):
        directory = self.parseDirectory(url)
        directory = directory[0]
        #Following code from stackoverflow.com
        for the_file in os.listdir(directory):
            file_path = os.path.join(directory, the_file)
            try:
                os.unlink(file_path)
            except Exception, e:
                print e

    def testCache(self):
        aTree = self.sampleTree()
        aTree.show()
        self.storeCache(aTree)
        self.storeInLast3(101, 'http://www.aurl.com')
        self.storeInLast3(101, 'http://www.anotherurl.com')
        self.storeInLast3(101, 'http://www.anothernotherurl.com')
        self.storeInLast3(101, 'http://www.anothernothernothernothernotherurl.com')
        anotherTree = self.fetchCache(aTree.getUrl(0))
        anotherTree.show()

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
        pageTree = PageTree()
        pageTree.createPageNode("http://www.dummyurl.com/timeStampTest.html", 0)
        pageTree.setPullTS(0, "52")
        self.storeCache(pageTree)
        pageTree.setPullTS(0, "53+1/2")
        self.updateTimeStamp(pageTree)

    def testStrangeDirectory(self):
        pageTree = PageTree()
        pageTree.createPageNode("http://www.dummyurl.com/strangeDirectory.html/strangeDirectory.html")
        self.storeCache(pageTree)
        self.storeCache(pageTree)

    def sampleTree(self):
        pageTree = PageTree("http://www.dummyurl.com/sample/aPage.html")
        pageTree.setEncodeType(0, "Jibberish")
        pageTree.setContent(0, "Here is some content. Blah blah blah.", pageTree.getEncodeType(0))
        pageTree.setPullTS(0, "57")
        pageTree.setHash(0, "Doobop")
        return pageTree

    def testClearPage(self):
        sampleTree = self.sampleTree()
        self.storeCache(sampleTree)
        self.clearPage(sampleTree.getUrl(0))

def defaultPredData(comicId):
    directory = "../../cache/predictorInfo/" + str(comicId) + "/"
    shutil.copy2("../../cache/predictorInfo/predictorData.txt", directory)
        
if __name__ == '__main__':
    cache = Cache()

    cache.testClearPage()

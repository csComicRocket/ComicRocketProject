#Lucas Berge
#import string
#import SocketServer
#from http import server
#import sys
from threading import Thread
import F1Engine.crFunctions
from F1Engine import fetchHTTP
import SimpleHTTPServer
import BaseHTTPServer
import F1Engine.J2Engine.notification

class HTTPListener(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """ Waits for HTTP requests in a loop on separate thread 
        GETS requies special ComicID header specifying comic number
        POSTS require crFunction header specifying action"""
    def do_GET(self):
        try:
            comicId  = self.headers['comicId']
            url = self.parseUrl()
            tree = fetchHTTP.fetchHTTP(url, comicId)
            
        except Exception as e:
            print(e)
            self.send_error(500, 'Internal Server Error: Failed GET')
            
    def do_POST(self):
        try:
            crFn = self.headers['crFunction']
            
            if(crFn == 'resetPredData'):
                F1Engine.crFunctions.resetPredData(self.headers['comicId'])
            elif(crFn == 'lockPredData'):
                F1Engine.crFunctions.lockPredData(self.headers['comicId'])
            elif(crFn == 'unlockPredData'):
                F1Engine.crFunctions.unlockPredData(self.headers['comicId'])
            elif(crFn == 'setUpdateSchedule'):
                F1Engine.crFunctions.setUpdateSchedule(self.headers['comicId'], self.headers['data'])
            elif(crFn == 'invalidNotification'):
                F1Engine.crFunctions.invalidNotification(self.headers['url'])
            elif(crFn == 'newComicFilterList'):
                F1Engine.crFunctions.newComicFilterList(self.headers['comicId'], self.headers['data'])
            elif(crFn == 'newComicBlackList'):
                F1Engine.crFunctions.newComicBlackList(self.headers['comicId'], self.headers['data'])
            elif(crFn == 'histComicFilterList'):
                F1Engine.crFunctions.histComicFilterList(self.headers['url'], self.headers['data'])
            elif(crFn == 'histComicBlackList'):
                F1Engine.crFunctions.histComicBlackList(self.headers['url'], self.headers['data'])
            else:
                raise KeyError
            
        except KeyError:
            print "Invalid crFunction call"
            F1Engine.J2Engine.notification.notification("Invalid crFunction call")
        except Exception as e:
            print(e)
            self.send_error(500, 'Internal Server Error: Failed POST')

    def parseUrl(self):
            _host = self.headers['Host'].rsplit(':')[0]
            _path = self.path
            _url = ''.join(_host)
            _url += _path
            return _url
    
running = True

def runListener():
    try:
        HttpServer = BaseHTTPServer.HTTPServer(('',81), HTTPListener)
        print('starting HTTPListener...')
        #HttpServer.serve_forever(.5)
        while running:
            HttpServer.timeout = 2
            HttpServer.handle_request()
    except KeyboardInterrupt:
        print('^C received, shutting down...')
        HttpServer.socket.close()
        
if __name__ == '__main__':
    t = Thread(target=runListener, args=())
    t.start()

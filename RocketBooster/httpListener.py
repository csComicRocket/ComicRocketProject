#Lucas Berge
#import string
#import SocketServer
#from http import server
#import sys
from threading import Thread
from F1Engine.crFunctions import *
from F1Engine import fetchHTTP
import SimpleHTTPServer
import BaseHTTPServer

class HTTPListener(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """ Waits for HTTP requests in a loop on separate thread 
        GETS requies special ComicID header specifying comic number
        POSTS require crFunction header specifying action"""
    def do_GET(self):
        try:
            comicID  = self.headers['comicID']
            url = self.parseUrl()
            print url
            tree = fetchHTTP.fetchHTTP(url, comicID)
            
        except Exception as e:
            print(e)
            self.send_error(500, 'Internal Server Error: Failed GET')
            
    def do_POST(self):
        try:
            crFn = self.headers['crFunction']
            
            if(crFn == 'resetPredData'):
                resetPredData(self.headers['comicID'])
            elif(crFn == 'lockPredData'):
                lockPredData(self.headers['comicID'])
            elif(crFn == 'unlockPredData'):
                unlockPredData(self.headers['comicID'])
            elif(crFn == 'setUpdateSchedule'):
                setUpdateSchedule(self.headers['data'])
            elif(crFn == 'invalidNotification'):
                invalidNotification(self.headers['url'])
            
        except KeyError:
            print "Invalid API data"
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

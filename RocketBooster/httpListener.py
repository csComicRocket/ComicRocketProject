#Lucas Berge
import string
from threading import Thread
import F1Engine.crFunctions
import F1Engine.fetchHTTP
#from http import server
import SimpleHTTPServer
import SocketServer
import BaseHTTPServer
import sys

class HTTPListener(SimpleHTTPServer.SimpleHTTPRequestHandler):
    """ Waits for HTTP requests in a loop on separate thread 
        GETS requies special ComicID header specifying comic number
        POSTS require crFunction header specifying action"""
    def do_GET(self):
        try:
            url = self.parseUrl()
            tree = F1Engine.fetchHTTP.fetchHTTP(url)
            
        except Exception as e:
            print(e)
            self.send_error(500, 'Internal Server Error: Failed GET')
            
    def do_POST(self):
        try:
            crFn = self.headers['crFunction'].split(':')[0]
            comicID  = self.headers['comicID'].split(':')[0]
            
            if(crFn == 'resetPredData'):
                resetPredData(comicID)
            if(crFn == 'lockPredData'):
                lockPredData(comicID)
            if(crFn == 'unlockPredData'):
                unlockPredData(comicID)
            if(crFn == 'setUpdateSchedule'):
                setUpdateSchedule(comicID)
            
        except Exception as e:
            print(e)
            self.send_error(500, 'Internal Server Error: Failed POST')

    def parseUrl(self):
            _host = self.headers['Host'].split(':')[0]
            _path = self.path
            _url = ''.join(host)
            _url += _path
            return url
    
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
        HttpServer.socket.close(self)
        
if __name__ == '__main__':
    t = Thread(target=runListener, args=())
    t.start()

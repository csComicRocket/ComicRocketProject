#Lucas Berge
import string
from crFunctions import *
from threading import Thread
from F1Engine import fetchHTTP
from http import server

class HTTPListener(server.BaseHTTPRequestHandler):
	""" Waits for HTTP requests in a loop on separate thread """
	def do_GET(self):
		try:
			url = parseUrl()
			fetchHTTP(url)
			
		except Exception as e:
			print(e)
			self.send_error(500, 'Internal Server Error: Failed GET')
			
	def do_POST(self):
		try:
			crFn = self.headers['crFunction'].split(':')[0]
			arg  = self.headers['comicID'] #need lookup for comicID
			
			if(crFn == 'resetPredData'):
				resetPredData(arg)
			if(crFn == 'lockPredData'):
				lockPredData(arg)
			if(crFn == 'unlockPredData'):
				unlockPredData(arg)
			if(crFn == 'setUpdateSchedule'):
				setUpdateSchedule(arg)
			
		except Exception as e:
			print(e)
			self.send_error(500, 'Internal Server Error: Failed POST')

	def parseUrl(self):
			_host = self.headers['Host'].split(':')[0]
			_path = self.path
			_url = ''.join(host)
			_url += _path
			return url
	
def runListener():
	try:
		HttpServer = server.HTTPServer(('',80), HTTPListner)
		print('starting HTTPListner...')
		HttpServer.serve_forever(.5)
	except KeyboardInterrupt:
		print('^C received, shutting down...')
		HttpServer.socket.close(self)
		
if __name__ == '__main__':
	t = Thread(target=runListener, args=())
	t.start()
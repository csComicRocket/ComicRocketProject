#Lucas Berge
import string
from threading import Thread
import F1Engine.crFunctions
import F1Engine.fetchHTTP
from http import server

class HTTPListener(server.BaseHTTPRequestHandler):
	""" Waits for HTTP requests in a loop on separate thread 
		GETS requies special ComicID header specifying comic number
		POSTS require crFunction header specifying action"""
	def do_GET(self):
		try:
			url = parseUrl()
			tree = fetchHTTP(url)
			
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
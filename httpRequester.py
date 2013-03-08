from httplib import HTTPConnection
from requests import data
import pika
from RocketBooster.F1Engine.J2Engine import globalVars
import logging
import sys
from threading import Thread
import time

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    handleMessage(body)    

def notifications():
    logging.basicConfig()
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=globalVars.host))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(callback, queue="hello", no_ack=True)
    channel.start_consuming()

def parseUrl(url):
    urlPieces = url.split("://")
    host = urlPieces[1].partition('/')[0]
    url = urlPieces[1].partition('/')[1] + urlPieces[1].partition('/')[2]
    return (host, url)

def handleMessage(msg):    
    url = parseUrl(msg)
    comicId = getComicId(url[0])
    httpRequest(url[0], url[1], comicId)
    latest = getLatest(url[0])
    if len(latest) == 0:
        with open("missed.txt", 'a+') as f:
            f.write("missed: " + msg)
        print "Bad Notification:", missed
    elif len(latest) > 1:
        with open("missed.txt", 'a+') as f:
            f.write("extra: " + msg)
    for l in latest:
        url = parseUrl(l)
        httpRequest(url[0], url[1], comicId)

def getComicId(host):
    with open("/usr/local/bin/comics.ids") as f:
        data = f.read()
    data = eval(data)
    if host:            
        return data[host]
    return data

def getLatest(host):
    latest = []
    with open("/usr/local/bin/" + host + ".list") as f:
        for line in f:
            latest.append(line.strip())
    with open("/usr/local/bin/" + host + ".list", 'w+') as f:
        pass
    return latest

def httpRequest(host, url, comicId):
    conn = HTTPConnection(host, 81)
    conn.request("GET", url, headers = {"comicID" : comicId})
    #r1 = conn.getresponse()

def getCaughtUp():
    hosts = getComicId(None)
    for h in hosts:
        latest = getLatest(h)
        for l in latest:
            url = parseUrl(l)
            httpRequest(url[0], url[1], hosts[h])
            time.sleep(1)

if __name__ == "__main__":
    t = Thread(target=getCaughtUp(), args=())
    t.start()
    try:
        notifications()
    except KeyboardInterrupt:
        t.join()
        sys.exit()
    
    

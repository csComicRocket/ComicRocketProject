from httplib import HTTPConnection
from requests import data
import pika
from RocketBooster.F1Engine.J2Engine import globalVars
import logging
import sys
from threading import Thread

missed = 0

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
    url = url.split("://")[1]
    host = url.partition('/')[0]
    url = url.partition('/')[1] + url.partition('/')[2]
    return (host, url)

def handleMessage(msg):    
    url = parseUrl(body)
    comicId = getComicId(url[0])
    httpRequest(url[0], url[1], comicId)
    latest = getLatest(url[0])
    if len(latest) == 0:
        global missed
        missed += 1
        print "Bad Notification:", missed
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
    conn = httplib.HTTPConnection(host, 81)
    conn.request("GET", url, headers = comicId)
    r1 = conn.getresponse()

def getCaughtUp():
    hosts = getComicId(None)
    for h in hosts:
        latest = getLatest(h)
        for l in latest:
            url = parseUrl(l)
            httpRequest(url[0], url[1], hosts[h])

if __name__ == "__main__":
    t = Thread(target=getCaughtUp(), args=())
    t.start()
    try:
        notifications()
    except KeyboardInterrupt:
        t.join()
        sys.exit()
    
    

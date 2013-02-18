from httplib import HTTPConnection
from requests import data
import pika

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

if __name__ == "__main__":
    channel.queue_declare(queue='hello')

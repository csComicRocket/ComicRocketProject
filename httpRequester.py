from httplib import HTTPConnection
from requests import data
import pika
from RocketBooster.F1Engine.J2Engine import globalVars
import logging

def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

if __name__ == "__main__":
    logging.basicConfig()
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=globalVars.host))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_consume(callback, queue="hello", no_ack=True)
    channel.start_consuming()
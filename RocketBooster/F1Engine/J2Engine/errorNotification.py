#Eric Smith
from datetime import datetime
import pika
import globalVars
import urllib

def errorNotification(error):
	""" Sends a notification that an error has been found using rabbitmq"""
        #INPROG
        
	# not final
	connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=globalvars.host))
        channel = connection.channel()

        channel.queue_declare(queue=globalvars.queue)

        channel.basic_publish(exchange='',
                              routing_key=globalvars.key,
                              body=error.read())

        #Test area, this just catches the message we sent

        def callback(ch, method, properties, body):
            print " [x] Received %r" % (body,)

        channel.basic_consume(callback,
                              queue=globalvars.queue,
                              no_ack=True)


	return None	
	


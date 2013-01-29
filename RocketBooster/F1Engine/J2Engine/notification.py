#Eric Smith
from datetime import datetime
import pika
import globalVars

def notification(comicURL):
	""" Sends a notification that a change has been found using rabbitmq, also maintains a list of recent url's/timestamps"""
        # opens the list, stores all but the last entry, overwrites the list with the new entry, appends with the old list
        # not totally safe might use a temp file
	f = open("notification_list",'r')
        #grabs all but the last line (deleting the last line)
	for i in range(999):
                old += f.readline()
        f.close()
        f = open("notification_list",'w')
        f.write(datetime.now()+";"+comicURL+"\n")
        f.close()
        f = open("notification_list",'a')
        f.write(old)
        f.close()
        
	# not final
	connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=globalvars.host))
        channel = connection.channel()

        channel.queue_declare(queue=globalvars.queue)

        channel.basic_publish(exchange='',
                              routing_key=globalvars.key,
                              body='IMPORTANT TEXT!')

        #Test area, this just catches the message we sent

        def callback(ch, method, properties, body):
            print " [x] Received %r" % (body,)

        channel.basic_consume(callback,
                              queue=globalvars.queue,
                              no_ack=True)


	return None	
	

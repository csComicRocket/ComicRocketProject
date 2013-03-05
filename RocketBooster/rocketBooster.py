import Scheduler
import httpListener
from threading import Thread
import sys
import time

if __name__ == "__main__":
    try:
        listener = Thread(target=httpListener.runListener, args=())
        listener.start()
        schedule = Thread(target=Scheduler.scheduler, args=())
        schedule.start()
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print "Closing Program..."
    finally:
        print "Terminating Processes..."
        httpListener.running = False
        Scheduler.running = False
        listener.join()
        schedule.join()
        print "All Processes Joined"
        sys.exit()
        print "Main thread ended"

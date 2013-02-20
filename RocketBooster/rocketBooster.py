import Scheduler
import httpListener
from threading import Thread
import sys

if __name__ == "__main__":
    try:
        listener = Thread(target=httpListener.runListener, args=())
        listener.start()
        Scheduler.scheduler()
    except KeyboardInterrupt:
        sys.exit()
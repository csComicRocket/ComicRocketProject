import Scheduler
import httpListener
from threading import Thread
import sys

if __name__ == "__main__":
    listener = Thread(target=httpListener.runListener, args=())
    comics = Thread(target=Scheduler.scheduler, args=())
    listener.start()
    comics.start()


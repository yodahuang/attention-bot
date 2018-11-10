import time
from zeromessage import EnvelopSocket
import sys

socket = EnvelopSocket.as_publisher()

while True:
    input('Press Enter to send a gaze')
    socket.publish('gaze', time.time())
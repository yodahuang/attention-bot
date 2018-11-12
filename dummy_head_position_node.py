import time
from zeromessage import EnvelopSocket
import sys

socket = EnvelopSocket.as_publisher()

while True:
    position = float(input('Please send head position (between 0 to 1)'))
    socket.publish('head/position', position)

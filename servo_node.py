import asyncio
from zeromessage import EnvelopSocket
from servo_interface.servo import Servo
import time
import argparse

parser = argparse.ArgumentParser(description='The node for serving servo')
parser.add_argument('--ip', required=True, help='The human position server ip')
args = parser.parse_args()

socket = EnvelopSocket.as_subscriber(ip=args.ip)


STEADY_TOL = 0.05
SERVO_STEP_SIZE = 2
TIMEOUT = 500  # ms

servo = Servo()
servo.go(90)  # Reset the servo at the beginning
current_angle = 90
last_received_time = None

human_right = True  # True means angle going up

@asyncio.coroutine
def searchDog():
    global current_angle, last_received_time, human_right
    while True:
        if last_received_time is None or (time.time() - last_received_time > TIMEOUT):
            print('Trigger searching mode')
            prev_angle = current_angle
            if human_right:
                current_angle += SERVO_STEP_SIZE
            else:
                current_angle -= SERVO_STEP_SIZE
            if (current_angle > 180 or current_angle < 0):
                human_right = not human_right
                current_angle = prev_angle
            servo.go(current_angle)
            yield from asyncio.sleep(0.1)

def servoHandler(position):
    global current_angle, last_received_time, human_right
    # print('Received: {}, Current position: {}'.format(position, current_angle))
    if abs(position - 0.5) < STEADY_TOL:
        return
    if position > 0.5:
        current_angle += SERVO_STEP_SIZE
        human_right = True
    else:
        current_angle -= SERVO_STEP_SIZE
        human_right = False
    servo.go(current_angle)
    last_received_time = time.time()

subscribe_coroutine = socket.subscribe('head/position', servoHandler)

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.gather(subscribe_coroutine(), searchDog()))

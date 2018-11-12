import asyncio
from zeromessage import EnvelopSocket
from servo_interface.servo import Servo

socket = EnvelopSocket.as_subscriber()

STEADY_TOL = 0.1
SERVO_STEP_SIZE = 5

servo = Servo()
servo.go(90)  # Reset the servo at the beginning
current_angle = 90

def servoHandler(position):
    global current_angle
    if abs(position - 0.5) < STEADY_TOL:
        return
    if position > 0.5:
        current_angle += SERVO_STEP_SIZE
    else:
        current_angle -= SERVO_STEP_SIZE
    servo.go(current_angle)


subscribe_coroutine = socket.subscribe('head/position', servoHandler)

asyncio.get_event_loop().run_until_complete(subscribe_coroutine())

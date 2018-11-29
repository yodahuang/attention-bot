import asyncio
import time
import click

from servo_interface.servo import Servo
from zeromessage import EnvelopSocket

STEADY_TOL = 0.05
SERVO_STEP_SIZE = 2
TIMEOUT = 500  # ms


class ServoManager:
    def __init__(self):
        self.servo = Servo()
        self.servo.go(90)
        self.current_angle = 90
        self.last_received_time = None
        self.human_is_on_right = True

    @asyncio.coroutine
    def search_dog(self):
        while True:
            if self.last_received_time is None or (time.time() - self.last_received_time > TIMEOUT):
                print('Trigger searching mode')
                prev_angle = self.current_angle
                if self.human_is_on_right:
                    self.current_angle += SERVO_STEP_SIZE
                else:
                    self.current_angle -= SERVO_STEP_SIZE
                if (self.current_angle > 180 or self.current_angle < 0):
                    self.human_is_on_right = not self.human_is_on_right
                    self.current_angle = prev_angle
                self.servo.go(self.current_angle)
                yield from asyncio.sleep(0.1)

    def posHandler(self, position):
        if abs(position - 0.5) < STEADY_TOL:
            return
        if position > 0.5:
            self.current_angle += SERVO_STEP_SIZE
            self.human_is_on_right = True
        else:
            self.current_angle -= SERVO_STEP_SIZE
            self.human_is_on_right = False
        self.servo.go(self.current_angle)
        self.last_received_time = time.time()

    def register(self, socket):
        subscribe_coroutine = socket.subscribe('head/position', self.posHandler)
        return asyncio.gather(subscribe_coroutine(), self.search_dog())


@click.command()
@click.option('--ip', default='localhost', help='The ip to connect to.')
@click.option('--port', default='5566', help='The port to connect to.')
def main(ip, port):
    socket = EnvelopSocket.as_subscriber(ip, port)
    servo_manager = ServoManager()

    asyncio.get_event_loop().run_until_complete(servo_manager.register(socket))


if __name__ == "__main__":
    main()

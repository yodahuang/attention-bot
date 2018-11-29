import asyncio
import time

import click

from assistant_interface.assistant import get_assistant
from zeromessage import EnvelopSocket


class StrictAssistant:
    def __init__(self):
        self.assistant = get_assistant()
        self.last_assist_time = time.time()

    def assist_once(self):
        while True:
            continue_conversation = self.assistant.assist()
            if not continue_conversation:
                break
        self.last_assist_time = time.time()
    
    def handle_gaze(self, gaze_timestamp):
        if (gaze_timestamp > self.last_assist_time):
            print('I received gaze')
            self.assist_once()


@click.command()
@click.option('--ip', default='localhost', help='The ip to connect to.')
@click.option('--port', default='5566', help='The port to connect to.')
def main(ip, port):
    socket = EnvelopSocket.as_subscriber(ip=ip, port=port)
    strict_assistant = StrictAssistant()
    subscribe_coroutine = socket.subscribe('gaze', strict_assistant.handle_gaze)
    asyncio.get_event_loop().run_until_complete(subscribe_coroutine())


if __name__ == "__main__":
    main()

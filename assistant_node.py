from zeromessage import EnvelopSocket
from assistant_interface.assistant import get_assistant
import time
import asyncio

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
            self.assist_once()
        else:
            print('Discarded old message')


def main():
    socket = EnvelopSocket.as_subscriber()
    strict_assistant = StrictAssistant()
    subscribe_coroutine = socket.subscribe('gaze', strict_assistant.handle_gaze)
    asyncio.get_event_loop().run_until_complete(subscribe_coroutine())

if __name__ == "__main__":
    main()
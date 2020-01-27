from channels.generic.websocket import WebsocketConsumer

import re

class CtrlConsumer(WebsocketConsumer):
    
    jog_regex = re.compile('J[UD]S\d')

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        # What even does close_code do?!?
        pass

    def receive(self, text_data):
        if self.jog_regex.match(text_data) is not None:
            print(text_data)
        else:
            print("Weird command received: " + text_data)

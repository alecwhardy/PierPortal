from channels.generic.websocket import WebsocketConsumer
from . import winch

import re
import logging

logger = logging.getLogger(__name__)

class CtrlConsumer(WebsocketConsumer):

    """This class stays static for the duration that the socket is connected"""
    
    jog_regex = re.compile('J[UD]S\d')
    home_regex = re.compile('[HB]')

    # The winch class uses class methods, so it doesn't need to be instantiated
    # We will never have more than one winch controller ever operating
    winch = winch.Winch()

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        if self.jog_regex.match(text_data) is not None:
            speed = int(text_data[3:])
            if text_data[1] == 'U':
                # We are jogging up
                self.winch.jog(-speed)
            if text_data[1] == 'D':
                # We are jogging down
                self.winch.jog(speed)

        elif self.home_regex.match(text_data) is not None:
            pass

        else:
            print("Weird command received: " + text_data)

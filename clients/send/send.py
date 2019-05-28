#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import datetime, os, random, string, sys
from proton import Message, Url
from proton.handlers import MessagingHandler
from proton.reactor import Container

class Send(MessagingHandler):
    def __init__(self):
        super(Send, self).__init__()
        self.rate = int(os.getenv("RATE", 1))

    def on_start(self, event):
        event.container.container_id = "send@%s" % os.getenv("HOSTNAME")
        conn = event.container.connect()
        address = os.getenv("ADDRESS", "test")
        self.sender = event.container.create_sender(conn, address, handler=self)

    def on_timer_task(self, event):
        sent = 0
        while self.sender.credit and sent < self.rate:
            msg = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
            self.sender.send(Message(body=msg))
            sent += 1
            print("%s %s" % (datetime.datetime.now(), msg))
        sys.stdout.flush()
        event.container.schedule(1, self)

    def on_link_opened(self, event):
        if event.sender == self.sender:
            event.container.schedule(1, self)

    def on_disconnected(self, event):
        print("disconnected")
        sys.stdout.flush()

try:
    Container(Send()).run()
except KeyboardInterrupt: pass




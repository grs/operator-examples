#!/usr/bin/env python

from __future__ import print_function, unicode_literals
import datetime, os, sys
from proton.handlers import MessagingHandler
from proton.reactor import Container

class Recv(MessagingHandler):
    def __init__(self):
        super(Recv, self).__init__()

    def on_start(self, event):
        event.container.container_id = "recv@%s" % os.getenv("HOSTNAME")
        conn = event.container.connect()
        address = os.getenv("ADDRESS", "test")
        event.container.create_receiver(conn, address)

    def on_link_opened(self, event):
        print("Listening on %s" % event.receiver.source.address)
        sys.stdout.flush()

    def on_message(self, event):
        print("%s %s" % (datetime.datetime.now(), event.message.body))
        sys.stdout.flush()

    def on_link_closed(self, event):
        print("No longer listening on %s" % event.source.address)
        sys.stdout.flush()

    def on_disconnected(self, event):
        print("disconnected")
        sys.stdout.flush()

try:
    Container(Recv()).run()
except KeyboardInterrupt: pass




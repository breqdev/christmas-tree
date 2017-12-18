import threading

import CHIP_IO.GPIO as io
from flask import Flask
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

app = Flask(__name__)

my_ip = "10.0.1.184"

@app.route("/")
def index():
    with open("websocket.html") as file:
        return file.read().replace("{my_ip}", my_ip)

relaypins = ["XIO-P0", "XIO-P1", "XIO-P2", "XIO-P3"]

class Relay:
    def __init__(self, pin):
        self.pin = pin
        io.setup(self.pin, io.OUT)

    def flip(self, value):
        io.output(self.pin, not value)

relays = [Relay(p) for p in relaypins]

class LightControl(WebSocket):

    def handleMessage(self):
        if len(self.data) < 2:
            return
        
        light, state = self.data[0], self.data[1]
        try:
            light = int(light)
        except:
            return
        assert 0 <= light <= 3
        
        try:
            state = int(state)
        except:
            return
        assert state == 0 or state == 1

        relay = relays[light]

        relay.flip(state)
        
    def handleConnected(self):
        print(self.address, "connected")

    def handleClose(self):
        print(self.address, "closed")

servesocket = lambda: SimpleWebSocketServer("", 2112, LightControl).serveforever()
servewebsite = lambda: app.run("0.0.0.0", port=80)

class WebSocketThread(threading.Thread):
    def run(self):
        servesocket()

WebSocketThread().start()
servewebsite()

import CHIP_IO.GPIO as io
from flask import Flask
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

app = Flask(__name__)

my_ip = "10.0.1.184"

relaypins = ["XIO-P0", "XIO-P1", "XIO-P2", "XIO-P3"]

class Relay:
    def __init__(self, pin):
        self.pin = pin
        io.setup(self.pin, io.OUT)

    def flip(self, value):
        io.output(self.pin, not value)

relays = [Relay(p) for p in relaypins]

@app.route("/<int:relay>/<int:state>")
def index(relay, state):
    relays[relay].flip(state)
    return "Consider it done."

app.run(host="0.0.0.0", port=80)

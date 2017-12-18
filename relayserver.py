import threading

from flask import Flask
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket

app = Flask(__name__)

my_ip = "localhost"

@app.route("/")
def index():
    with open("websocket.html") as file:
        return file.read().replace("{my_ip}", my_ip)

relays = ["XIO-P0", "XIO-P1", "XIO-P2", "XIO-P3"]

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

        print("Set relay {} to value {}".format(relay, state))

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

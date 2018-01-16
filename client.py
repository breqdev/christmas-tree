import requests

import CHIP_IO.GPIO as io

relaypins = ["XIO-P0", "XIO-P1", "XIO-P2", "XIO-P3"]

class Relay:
    def __init__(self, pin):
        self.pin = pin
        io.setup(self.pin, io.OUT)

    def flip(self, value):
        io.output(self.pin, not value)

relays = [Relay(p) for p in relaypins]

while True:
    status = requests.get("http://mc.2112electronics.com/").json()
    for i, s in enumerate(status):
        relays[i].flip(s)

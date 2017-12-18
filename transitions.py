import time
import CHIP_IO.GPIO as io
import random

interval = 5

relaypins = ["XIO-P0", "XIO-P1", "XIO-P2", "XIO-P3"]

class Relay:
    def __init__(self, pin):
        self.pin = pin
        io.setup(self.pin, io.OUT)

    def flip(self, value):
        io.output(self.pin, not value)

relays = [Relay(p) for p in relaypins]

old_config = 0

while True:
    config = random.randint(0, 15)
    transitioning = config ^ old_config
    for i in range(4):
        if transitioning & 2**i:
            relays[i].flip(config & 2**i)
            time.sleep(0.3)
    n = old_config = config
    c = 0
    while n:
        c += 1
        n &= n - 1

    time.sleep(60 if (config + 1) % 16 == 0 else 0)

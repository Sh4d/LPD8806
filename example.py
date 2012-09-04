#!/usr/bin/python

from time import sleep
import LPD8806

led = LPD8806.strand()

while True:
    for i in range(5):
        led.fill(255, 0, 0)
        led.update()
        sleep(0.3)
        led.fill(0, 255, 0)
        led.update()
        sleep(0.3)
        led.fill(0, 0, 255)
        led.update()
        sleep(0.3)

    for i in range(300):
        led.wheel()
        led.update()

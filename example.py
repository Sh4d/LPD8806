#!/usr/bin/python

from time import sleep
from LPD8806 import LPD8806

led = LPD8806(160)

while True:
	led.fill(255, 0, 0)
	sleep(1)
	led.fill(0, 255, 0)
	sleep(1)
	led.fill(0, 0, 255)
	sleep(1)

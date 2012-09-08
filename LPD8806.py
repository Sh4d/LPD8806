#!/usr/bin/env python

"""
LPD8806.py: Raspberry Pi library for the Adafruit LPD8806 RGB Strand

Provides the ability to drive a LPD8806 based strand of RGB leds from the
Raspberry Pi

Colors are provided as RGB and converted internally to the strand's 7 bit
values.

The leds are available here: http://adafruit.com/products/306

Wiring:
    Pi MOSI -> Strand DI
    Pi SCLK -> Strand CI

Make sure to use an external power supply to power the strand

Example:
    >> import LPD8806
    >> led = LPD8806.strand()
    >> led.fill(255, 0, 0)
"""


class strand:

    def __init__(self, leds=160, dev="/dev/spidev0.0"):
        """
        Variables:
            leds -- strand size
            dev -- spi device
        """
        self.dev = dev
        self.spi = file(self.dev, "wb")
        self.leds = leds
        self.gamma = bytearray(256)
        self.buffer = [0 for x in range(self.leds)]
        self.wheelOffset = 0
        for led in range(self.leds):
            self.buffer[led] = bytearray(3)
        for i in range(256):
            # Color calculations from
            # http://learn.adafruit.com/light-painting-with-raspberry-pi
            self.gamma[i] = 0x80 | int(
                pow(float(i) / 255.0, 2.5) * 127.0 + 0.5
            )

    def fill(self, r, g, b, start=0, end=0):
        """
        Fill the strand (or a subset) with a single color
        """
        if start < 0:
            raise NameError("Start invalid:" + str(start))
        if end == 0:
            end = self.leds
        if end > self.leds:
            raise NameError("End invalid: " + str(end))
        for led in range(start, end):
            self.buffer[led][0] = self.gamma[g]
            self.buffer[led][1] = self.gamma[r]
            self.buffer[led][2] = self.gamma[b]

    def set(self, pixel, r, g, b):
        """
        Set a single LED a specific color
        """
        self.buffer[pixel][0] = self.gamma[g]
        self.buffer[pixel][1] = self.gamma[r]
        self.buffer[pixel][2] = self.gamma[b]

    def update(self):
        """
        Flush the buffer to the strand
        """
        for x in range(self.leds):
            self.spi.write(self.buffer[x])
            self.spi.flush()
        self.spi.write(bytearray(b'\x00'))
        self.spi.flush()

    def wheel(self, start=0, end=0):
        """
        Generate a moving color wheel between a start and end
        """
        if end == 0:
            end = self.leds
        size = end - start
        self.wheelOffset += 1
        if self.wheelOffset == 384:
            self.wheelOffset = 0
        for i in range(size):
            color = (i * (384 / size) + self.wheelOffset) % 384
            if color < 128:
                r = 127 - color % 128
                g = color % 128
                b = 0
            elif color < 256:
                g = 127 - color % 128
                b = color % 128
                r = 0
            else:
                b = 127 - color % 128
                r = color % 128
                g = 0
            self.set(start + i, r, g, b)
        self.update()

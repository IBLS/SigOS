#
# Defines Hardware interfaces for SigOS
#
# Copyright (C) 2021-2024 Daris A Nevil - International Brotherhood of Live Steamers
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# DARIS A NEVIL, OR ANY OTHER CONTRIBUTORS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
#

# Nomenclature: B, B-, B+
# B means the block protected by the semaphore
# B- means the block immediately preceeding the protected block B
# B+ means the block immediately following the protected block B
# This nomenclature is in respect to the direction of the train
# moving from B- into B and viewing the semaphore's face

import sys
import machine
from machine import Pin, PWM
import ubinascii
import Semaphore
import Light
import WS281

class Hardware:

    # Class variable that holds the singleton instance of Hardware
    c_hardware = None

    # Determine underlying hardware and initialize pins
    #
    def __init__(self):
        self.m_platform = sys.platform
        self.m_unique_id = ubinascii.hexlify(machine.unique_id())

        if (self.m_platform == 'esp8266'):
            # ESP8266 pinout
            # Pin 1 - GND
            # Pin 2 - On-board LED and WS281 for lights/LED
            # Pin 3 - Detect B
            # Pin 4 - Detect B-
            # Pin 5 - Servo control out - GND at power-on to program
            # Pin 6 - /Reset (unused)
            # Pin 7 - Detect B+
            # Pin 8 - VCC
            self.m_detect_b  = Pin(3, Pin.IN, Pin.PULL_UP)
            self.m_detect_bm = Pin(4, Pin.IN, Pin.PULL_UP)
            self.m_detect_bp = Pin(7, Pin.IN, Pin.PULL_UP)
        elif (self.m_platform == "esp32"):
            # ESP32 S2 mini pins used - tries to use same "pin" numbers as ESP8266
            # Pin 2 - LED light
            # Pin 3 - detect block B
            # Pin 4 - detect block B-
            # Pin 5 - Servo control out
            # Pin 6 - ADC1_0 Light Level Detector
            # Pin 7 - detect block B+
            self.m_detect_b  = Pin(3, Pin.IN, Pin.PULL_UP)
            self.m_detect_bm = Pin(4, Pin.IN, Pin.PULL_UP)
            self.m_detect_bp = Pin(7, Pin.IN, Pin.PULL_UP)
        else:
            raise Exception('Unrecognized hardware {} 02407241136', self.m_platform)

        # Save this singleton instance
        Hardware.c_hardware = self


    # @returns True if the B input signal has detected a train
    #
    def get_detect_b(self):
        return self.m_detect_b.value()


    # @returns True if the B- input signal has detected a train
    #
    def get_detect_bm(self):
        return self.m_detect_bm.value()


    # @returns True if the B+ input signal has detected a train
    #
    def get_detect_bp(self):
        return self.m_detect_bp.value()


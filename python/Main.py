#
# Main startup for SigOS
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

import sys
import network
import time

WIFI_SSID = "IGNRR"
WIFI_PASSWD = "downcase"

def do_connect():
    wlan = network.WLAN(network.STA_IF) # create station interface
    wlan.active(True)       # activate the interface
    if (sys.platform == 'esp8266'):
        # txpower Not support in ESP8266
        pass
    else:
        print("txpower={}", wlan.config('txpower'))
        wlan.config(txpower=7.0)
        print("txpower={}", wlan.config('txpower'))
    if not wlan.isconnected():      # check if the station is connected to an AP
        wlan.connect(WIFI_SSID, WIFI_PASSWD) # connect to an AP

        for _ in range(20):
            if wlan.isconnected():      # check if the station is connected to an AP
                break
            print('.', end='')
            time.sleep(0.5)
        else:
            print(" Connect attempt timed out\n")
            return
    print('\nnetwork config:', wlan.ifconfig())

do_connect()

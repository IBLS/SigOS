#
# WiFi Control for SigOS
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
import Log

class WiFi:

    # The class object holding the singleton WiFi object
    c_wifi = None

    # Intialize the object as a Station that will connect to a Router
    # or Access Point
    #
    def __init__(self, p_ssid, p_password, p_hostname):
        self.m_ssid = p_ssid
        self.m_password = p_password
        self.m_hostname = p_hostname

        self.m_wifi = network.WLAN(network.STA_IF)
        #self.m_wifi = network.WLAN(network.AP_IF)
        self.m_wifi_ip = None
        self.m_wifi_mask = None
        self.m_wifi_router = None
        self.m_wifi_dns = None
        self.m_log = Log.Log()
        WiFi.c_wifi = self


    # Attempt to connect to the Router/AP.
    # @returns True on successful connection, returns False if Router/AP not found
    #
    def connect(self):
        if not self.m_wifi.isconnected():
            s = 'WiFi connecting to network...'
            self.m_log.add(self.m_hostname, s)
            print(s)
            self.m_wifi.active(True)

            # Limit the transmit power, otherwise the board will reboot
            if (sys.platform == 'esp8266'):
                # txpower Not support in ESP8266
                pass
            else:
                s = "default txpower=" + str(self.m_wifi.config('txpower'))
                self.m_log.add(self.m_hostname, s)
                print(s)
                self.m_wifi.config(txpower = 7.0)
                s = "configured txpower=" + str(self.m_wifi.config('txpower'))
                self.m_log.add(self.m_hostname, s)
                print(s)

            # Set hostname
            self.m_wifi.config(dhcp_hostname = self.m_hostname)

            time.sleep(1)
            self.m_wifi.connect(self.m_ssid, self.m_password)

            # Wait here until connected
            while (True):
                #print("status={}", self.m_wifi.status())
                if self.m_wifi.isconnected():
                    break

        # Get my DHCP configuration
        config = self.m_wifi.ifconfig()
        self.m_log.add(self.m_hostname, str(config))
        print('wifi config: {}', config)
        self.m_wifi_ip = config[0]
        self.m_wifi_mask = config[1]
        self.m_wifi_router = config[2]
        self.m_wifi_dns = config[3]

        return True


    # Disconnect from the WiFi Router/AP
    #
    def disconnect(self):
        # Disconnect from wifi
        self.m_wifi.active(False)


    async def poll(self):
        if self.m_wifi.isconnected():
            await uasyncio.sleep(0)
            return True
        else:
            return self.connect()


    # Destructor will disconnect
    #
    def __del__(self):
        self.m_wifi.disconnect()


    # @returns A string representation of this WiFi object
    #
    def __str__(self):
        s = "ssid:"
        s += self.m_ssid
        s += ",password:"
        s += self.m_password
        s += ",hostname:"
        s += self.m_hostname
        config = self.m_wifi.ifconfig()
        s += ',config:'
        s += config


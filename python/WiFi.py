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

import network

class WiFi:

    # Intialize the object as a Station that will connect to a Router
    # or Access Point
    #
    def __init__(self):
        self.m_sta_if = network.WLAN(network.STA_IF)
        self.m_sta_ip = None
        self.m_sta_mask = None


    # Attempt to connect to the Router/AP.
    # @returns True on successful connection, returns False if Router/AP not found
    #
    def connect(self):
        if not self.m_sta_if.isconnected():
            print('connecting to network...')
            self.m_sta_if.active(True)
            self.m_sta_if.connect('IGNRR', 'downcase')
            if (not self.m_sta_if.isconnect()):
                return False
        addr4 = self.m_sta_if.ipconfig('addr4')
        self.m_sta_ip = addr[0]
        self.m_sta_mask = addr[1]
        print('network config: %', self.m_sta_ip)
        return True


    # Disconnect from the WiFi Router/AP
    #
    def disconnect(self):
        # Disconnect from wifi
        self.m_sta_if.active(False)


    # Destructor will disconnect
    #
    def __del__(self):
        self.m_sta_if.disconnect()



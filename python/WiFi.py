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
import machine
import ntptime
import Log
import Config


class WiFi:

    # The class object holding the singleton WiFi object
    c_wifi = None

    # Intialize the object as a Station that will connect to a Router
    # or Access Point
    # @param p_config Reference to the main Configuration object
    # @param p_log Reference to the main Log object
    #
    def __init__(self, p_config, p_log):
        self.m_config = p_config
        self.m_log = p_log
        self.m_ssid = p_config.m_wifi_ssid
        self.m_password = p_config.m_wifi_password
        self.m_hostname = p_config.m_hostname

        self.m_wifi = network.WLAN(network.STA_IF)
        #self.m_wifi = network.WLAN(network.AP_IF)
        self.m_wifi_ip = None
        self.m_wifi_mask = None
        self.m_wifi_router = None
        self.m_wifi_dns = None

        # Update using NTP every hour
        self.m_ntp_update_sec = 1 * 60 * 60
        # Last time an NTP update occurred
        self.m_ntp_last_update = 0

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
            print("Setting hostname:", self.m_hostname)
            wifi_hostname = self.m_hostname
            no_local = self.m_hostname.split(".")
            if no_local.pop() == "local":
                wifi_hostname = no_local[0]
            #print("Setting wifi_hostname:", wifi_hostname)
            self.m_wifi.config(dhcp_hostname = wifi_hostname)

            time.sleep(1)
            self.m_wifi.connect(self.m_ssid, self.m_password)

            # Wait here until connected
            while (True):
                #print("status={}", self.m_wifi.status())
                if self.m_wifi.isconnected():
                    break

        # Update time with NTP
        self.update_clock_ntp()

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


    # Perform periodic tasks here, called from Main.py loop
    #
    async def poll(self):
        # Reconnect if we lost connectivity
        if not self.m_wifi.isconnected():
            return self.connect()

        # Perform Wifi background processing
        await uasyncio.sleep(0)

        # Time to update local clock from NTP?
        self.update_clock_ntp()

        return True



    # Provide the Received Signal Strength Indicator
    # Returned value is between 0dBm (strongest)
    # and -255dBm (weakest)
    #
    def get_rssi_dbm(self):
        rssi = -255
        try:
            rssi = self.m_wifi.status('rssi')
        except:
            rssi = -255
        return rssi


    # Get one of serveral WiFi parameters.
    # @param p_param The string name of the parameter, including:
    #   mac - MAC Address
    #   ssid - WiFi access point name
    #   channel - WiFi Channel
    #   hidden - True if SSID is hidden
    #   security - Security protocol supported
    #   key - Access key
    #   reconnects - Number of reconnect attempts to make
    #   txpower - Max transmit power in dBm
    #   pm - WiFi Power Management setting
    # @returns A string result
    #
    def get_config(self, p_param):
        msg = p_param
        msg += ': '
        result = None
        try:
            result = self.m_wifi.config(p_param)
        except:
            # Parameter not supported
            return None

        if p_param == 'mac':
            msg += '{:02x}:'.format(result[0])
            msg += '{:02x}:'.format(result[1])
            msg += '{:02x}:'.format(result[2])
            msg += '{:02x}:'.format(result[3])
            msg += '{:02x}:'.format(result[4])
            msg += '{:02x}'.format(result[5])
        elif p_param == 'security':
            if result == 0:
                msg += 'open'
            elif result == 1:
                msg += 'WEP'
            elif result == 2:
                msg += 'WPA-PSK'
            elif result == 3:
                msg += 'WPA2-PSK'
            elif result == 4:
                msg += 'WPA/WPA2-PSK'
            else:
                msg += 'unknown'
        elif p_param == 'hidden':
            if result == 0:
                msg += 'visible'
            else:
                msg += 'hidden'
        elif p_param == 'reconnects':
            if result == 0:
                msg += 'none'
            elif result < 0:
                msg += 'unlimited'
            else:
                msg += str(result)
        elif p_param == 'txpower':
            msg += str(result)
            msg += 'dBm'
        elif p_param == 'pm':
            if result == network.WLAN.PM_PERFORMANCE:
                msg += 'Performance'
            elif result == network.WLAN.PM_POWERSAVE:
                msg += 'PowerSave'
            elif result == network.WLAN.PM_NONE:
                msg += 'No Power Management'
            else:
                msg += 'unknown'
        else:
            msg += str(result)

        return msg
        

    # Update the local clock using NTP protocol
    #
    def update_clock_ntp(self):
        # Time to update local clock from NTP?
        if time.time() > self.m_ntp_last_update:
            ntptime.host = self.m_config.m_ntp_host
            ntptime.timeout = self.m_config.m_ntp_timeout_sec
            ntptime.settime()
            if self.m_config.m_tz_offset_sec:
                # Adjust for Timezone
                new_time = time.time()
                new_time = new_time + self.m_config.m_tz_offset_sec
                tm = time.gmtime(new_time)
                machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
            self.m_ntp_last_update = time.time() + self.m_ntp_update_sec


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


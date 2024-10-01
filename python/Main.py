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

#import sys
#import network
#import uasyncio
import time
import WiFi
import TelnetServer
import Config
import Commands
import Command

def get_config():
    config = Config.Config("config.json")

get_config()

g_wifi = None
g_telnet_server = None

def do_connect():
    ssid = Config.Config.c_config.m_wifi_ssid
    password = Config.Config.c_config.m_wifi_password
    hostname = Config.Config.c_config.m_hostname
    global g_wifi
    g_wifi = WiFi.WiFi(ssid, password, hostname)
    g_wifi.connect()

    global g_telnet_server
    g_telnet_server = TelnetServer.TelnetServer()

    welcome = hostname + " " + str(g_wifi.m_wifi_ip) + "\r\n"
    g_telnet_server.set_welcome(welcome)

    g_telnet_server.start()

do_connect()

def loop():

    buf = bytearray(512)
    while (True):

        g_wifi.poll()
        g_telnet_server.poll()
        #print("sleeping...\n")
        #time.sleep(1)
        #continue
 
        # Check for traffic from each Telnet clinet
        client_list = TelnetServer.TelnetConn.c_wrapper_list
        for client in client_list:
            len = client.readinto(buf)
            # print("len=", len)
            keeplinebreaks = False
            lines = buf[0:len].splitlines(keeplinebreaks)
            for line in lines:
                # Attempt to parse and execute the specified command line
                # print(line)
                s = line.decode()
                word_list = s.split(" ")
                (cmd_match, func_result, result_list) = Command.Command.ParseAndExec(word_list)
                if (not cmd_match):
                    pass
                if (not func_result):
                    result_list.append('Command failed')
                for out_line in result_list:
                    try:
                        client.m_client_socket.write(out_line)
                        client.m_client_socket.write("\r\n")
                    except Exception as e:
                        # Log the error
                        pass
                client.prompt()

        # Sleep at end of the loop to let other code run
        print("sleeping...\n")
        time.sleep(0.5)

loop()


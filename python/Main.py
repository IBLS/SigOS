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

import time
import Config
import Log
import TelnetServer
import WiFi
import Commands
import Command
import Rules
import Semaphore
import Light
import LightLevel
import WS281
import Detector

# Initialize logger
g_log = Log.Log()

# Load the configuration file
#
print("Loading config")
g_config = Config.Config("config.json", g_log)
Log.Log.SetConfig(g_config)

# Initialize hardware
WS281.WS281.InitHardware(g_config, Light.Light.Count(), g_log)
Semaphore.Semaphore.InitHardware(g_config)
Light.Light.InitHardware(g_config)
LightLevel.LightLevel.InitHardware(g_config, g_log)
Detector.Detector.InitHardware()


# Load the rules from the file specified in the config file
#
print("Loading rules from", g_config.m_rules_file)
g_rules = Rules.Rules(g_config.m_rules_file, g_config, g_log)


g_wifi = None
g_telnet_server = None

def do_connect():
    global g_config
    global g_wifi
    g_wifi = WiFi.WiFi(g_config, g_log)
    g_wifi.connect()

    global g_telnet_server
    g_telnet_server = TelnetServer.TelnetServer()

    welcome = g_config.m_hostname + " " + str(g_wifi.m_wifi_ip) + "\r\n"
    g_telnet_server.set_welcome(welcome)

    g_telnet_server.start()

do_connect()


# Initialzie the Rules state machine
g_rules.startup(g_config.m_hostname)


def loop():

    print("Accepting connections")
    buf = bytearray(512)
    # Time between polls
    poll_time = 0.2
    while (True):

        g_wifi.poll()
        #g_telnet_server.poll()
        Detector.Detector.Poll()
 
        # Check for traffic from each Telnet clinet
        client_list = TelnetServer.TelnetConn.c_wrapper_list
        for client in client_list:
            len = client.readinto(buf)
            # Get the string name of Telnet client (usually its IP address)
            source = str(client.m_client_addr)
            # print("len=", len)
            keeplinebreaks = False
            lines = buf[0:len].splitlines(keeplinebreaks)
            for line in lines:
                # Convert binary buffer to string
                line_decoded = line.decode()
                # Attempt to parse and execute the specified command line
                # print(line)
                (cmd_match, func_result, result_list) = Command.Command.ParseAndExec(line_decoded, source)
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
        #print("sleeping...\n")
        time.sleep(poll_time)

loop()


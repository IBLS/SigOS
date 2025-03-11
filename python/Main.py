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

from machine import Pin
from machine import WDT
import sys
import time
import Config
import Log
import TelnetServer
import WiFi
import Commands
import Command
import Rules
import Semaphore
import GPIO
import Light
import LightLevel
import WS281
import Detector
import StateConfig
import StateMachine

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

# Setup the on-board pushbutton to drop to REPL
g_repl_button = GPIO.GPIO("REPLButton", 0, Pin.IN, Pin.PULL_UP, g_log)


# Load the rules from the file specified in the config file
#
print("Loading rules from", g_config.m_rules_file)
g_rules = Rules.Rules(g_config.m_rules_file, g_config, g_log)


# Load state machines, if any
print("Loading state machines")
StateConfig.StateConfig(g_config.m_state_file, g_config.m_hostname, g_log)
StateMachine.StateMachine.Print()

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

# Init and start the watchdog
print("Platform =", sys.platform)
g_wdt = None
if sys.platform == 'esp8266':
    # ESP8266 does not allow timeout to be specified
    # See https://www.engineersgarage.com/micropython-esp8266-esp32-watchdog-timer-wdt/
    g_wdt = WDT()
    pass
elif sys.platform == 'esp32':
    g_wdt = WDT(timeout=2000)
else:
    raise Exception('Unrecognized hardware ', sys.platform, '02407241136')

def loop():

    print("Accepting connections")
    # Time between polls
    poll_time = 0.2
    while (True):

        # Not dead (yet), feed the watchdog
        g_wdt.feed()

        # Test for REPL button
        if g_repl_button.m_pin.value() == 0:
            raise ValueError('Entering REPL')

        # Perform polls
        g_wifi.poll()
        #g_telnet_server.poll()
        Detector.Detector.Poll()
        StateMachine.StateMachine.Poll(poll_time)
        TelnetServer.TelnetConn.Poll()
 
        # Sleep at end of the loop to let other code run
        #print("sleeping...\n")
        time.sleep(poll_time)

loop()


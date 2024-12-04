#
# Class representing and managing Detectors
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

import machine
from machine import Pin
import Config
import TargetedCommand
import GPIO
import Log
import Timestamp


class Detector:

    # Store each created Detector in this class list
    c_detector_list = list()


    # Create a new detector
    # @param p_detector_config Base of the parsed json Detector
    # @param p_hostname Hostname of this signal
    # @param p_log References the logging object
    #
    def __init__(self, p_detector_config, p_hostname, p_log):

        self.m_hostname = p_hostname
        self.m_log = p_log
        self.m_detector_name = p_detector_config["detector-name"]
        self.m_gpio_pin = p_detector_config["gpio-pin"]
        self.m_gpio_pull = p_detector_config["gpio-pull"]
        self.m_gpio_pull_pin = None
        self.m_active_hi = p_detector_config["active-hi"]
        self.m_active_soak_sec = p_detector_config["active-soak-sec"]
        self.m_active_hold_sec = p_detector_config["active-hold-sec"]
        self.m_inactive_soak_sec = p_detector_config["inactive-soak-sec"]
        self.m_inactive_hold_sec = p_detector_config["inactive-hold-sec"]
        self.m_soak_state = None
        self.m_soak_timestamp = None
        self.m_hold_timestamp = None
        self.m_current_state = None
        self.m_switch = 0

        if self.m_active_hi.lower() == "true":
            self.m_active_hi = True
        else:
            self.m_active_hi = False

        if self.m_gpio_pull.lower() == "up":
            self.m_gpio_pull_pin = Pin.PULL_UP
        elif self.m_pgio_pull.lower() == "down":
            self.m_gpio_pull_pin = Pin.PULL_DOWN
        else:
            msg = 'Invalid value for gpio-pull: "'
            msg += self.m_gpio_pull
            msg += '" 202411211204'
            self.m_log.add("Detector", msg)

        self.m_active_cmd_list = list()
        active_cmds = p_detector_config["active-cmds"]
        for active_cmd in active_cmds:
            target = active_cmd["target"]
            cmd = active_cmd["cmd"]
            target = TargetedCommand.TargetedCommand(target, cmd, self.m_hostname, self.m_log)
            self.m_active_cmd_list.append(target)

        self.m_inactive_cmd_list = list()
        inactive_cmds = p_detector_config["inactive-cmds"]
        for inactive_cmd in inactive_cmds:
            target = inactive_cmd["target"]
            cmd = inactive_cmd["cmd"]
            target = TargetedCommand.TargetedCommand(target, cmd, self.m_hostname, self.m_log)
            self.m_inactive_cmd_list.append(target)

        # Detect duplications
        for detector in Detector.c_detector_list:
            if self.m_detector_name == detector.m_detector_name:
                msg = 'Duplicate detector name: "'
                msg += self.m_detector_name
                msg += '" 202411211239'
                self.m_log.add("Detector", msg)

        Detector.c_detector_list.append(self)


    # Destructor
    #
    def __del__(self):
        pass


    # Initialize the hardware associated with the detectors
    # Call this method only after loading all Config
    #
    @classmethod
    def InitHardware(p_class):
        for detector in p_class.c_detector_list:
            detector.init_hardware()


    # Initialize Detector hardware
    #
    def init_hardware(self):
        # Configure the detector's gpio pin
        #self.m_gpio = Pin(self.m_gpio_pin, Pin.IN, self.m_gpio_pull_pin)
        owner = self.ident()
        self.m_gpio = GPIO.GPIO(owner, self.m_gpio_pin, Pin.IN, self.m_gpio_pull_pin, self.m_log)
        return


    # Perform periodic polling for all of the registered Detectors.
    # Call this method only after loading all Config
    #
    @classmethod
    def Poll(p_class):
        for detector in p_class.c_detector_list:
            detector.poll()


    # Poll the detector gpio pin and test for soak and hold times.
    # Execute commands if a new state is declared.
    #
    def poll(self):
        # Get current pin state
        state = self.m_gpio.m_pin.value()

        if self.m_switch == 0:
            # Initialization
            self.m_soak_state = None
            self.m_soak_timestamp = None
            self.m_hold_timestamp = None
            self.m_current_state = None
            self.m_switch = 1

        if self.m_switch == 1:
            # Start a new soak state and time
            self.m_soak_state = state
            self.m_soak_timestamp = Timestamp.Timestamp()
            if state == self.m_active_hi:
                self.m_soak_timestamp.expire_after(self.m_active_soak_sec)
            else:
                self.m_soak_timestamp.expire_after(self.m_inactive_soak_sec)
            self.m_switch = 2
            return

        if self.m_switch == 2:
            if state != self.m_soak_state:
                # Input has changed during soak, circle back
                # around and restart soak with new state
                self.m_switch = 1
                return

            # Input still matches soak state
            if self.m_soak_timestamp.expired():
                # Soak state has completed, delcare current state
                # and start hold time and execute actions
                self.m_current_state = state
                self.m_soak_state = None
                self.m_soak_timestamp = None
                self.m_hold_timestamp = Timestamp.Timestamp()
                if self.m_current_state == self.m_active_hi:
                    self.m_hold_timestamp.expire_after(self.m_active_hold_sec)
                    self.execute_cmds(self.m_active_cmd_list)
                else:
                    self.m_hold_timestamp.expire_after(self.m_inactive_hold_sec)
                    self.execute_cmds(self.m_inactive_cmd_list)

                # Transition to hold state
                self.m_switch = 3
                return

            if self.m_switch == 3:
                # Hold state
                if self.m_hold_timestamp.expired():
                    # Hold time has expired, now eligible for change
                    self.m_hold_timestamp = None
                    self.m_switch = 4
                return

            if self.m_switch == 4:
                # Waiting here for detector change of state
                if state == self.m_current_state:
                    # No change in state
                    return

                # Detected state change, circle around to soak
                self.m_switch = 1
                return

            if self.m_switch > 4:
                # Invalid switch
                raise Exception("Invalid detector switch  202412021835")
                self.m_switch = 0

            return


    # Execute commands for the newly declared state
    # @param p_cmd_list A list of commands to execute
    #
    def execute_cmds(self, p_cmd_list):
        for target in p_cmd_list:
            target.execute()


    # Provide an identifier for this object
    #
    def ident(self):
        id = "Detector(pin="
        id += str(self.m_gpio_pin)
        id += "):"
        id += str(self.m_detector_name)
        return id


    # @returns A string representation of this Detector
    #
    def __str__(self):
        s = "detector:"
        s += str(self.m_detector_name)
        s += ", gpio-pin:"
        s += str(self.m_gpio_pin)
        s += ", gpio-pull:"
        s += str(self.m_gpio_pull)
        s += ", active-hi:"
        s += str(self.m_active_hi)
        return s



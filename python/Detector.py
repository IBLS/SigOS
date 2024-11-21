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
import Pin
import Config
import Log


class Detector:

    # Store each created Detector in this class list
    c_detector_list = list()


    # Create a new detector
    # @param p_detector_config Base of the parsed json Detector
    # @param p_log References the logging object
    #
    def __init__(self, p_detector_config, p_log):

        self.m_log = p_log
        self.m_detector_name = p_detector_config["detector-name"]
        self.m_gpio_pin    = p_detector_config["gpio-pin"]
        self.m_gpio_pull   = p_detector_config["gpio-pull"]
        self.m_gpio_pull_pin = None
        self.m_active_hi   = p_detector_config["active-hi"]

        if self.m_gpio_pull.lower() == "up":
            self.m_gpio_pull_pin = Pin.PULL_UP
        elif: self.m_pgio_pull.lower() == "down":
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
            target = Target.Target(target, cmd)
            self.m_active_cmd_list.append(target)

        self.m_inactive_cmd_list = list()
        inactive_cmds = p_detector_config["inactive-cmds"]
        for inactive_cmd in inactive_cmds:
            target = inactive_cmd["target"]
            cmd = inactive_cmd["cmd"]
            target = Target.Target(target, cmd)
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
    # Call this method after loading all Config
    #
    @classmethod
    def InitHardware(p_class):
        for detector in p_class.c_detector_list:
            detector.init_hardware()


    # Called by interrupt handler when a gpio detector pin changes state
    # @param p_class This class
    # @param p_pin The Pin value of the gpio causing the interrupt
    #
    @classmethod
    def PinChangeState(p_class, p_pin)
        for detector in p_class.c_detector_list:
            if self.m_pin == p_pin:
                detector.change_state_interrupt()
                return


    # Provide an identifier for this object
    #
    def ident(self):
        id = "Detector(pin="
        id += self.m_gpio_pin
        id += "):"
        id += self.m_detector_name
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


    # Initialize Detector hardware
    #
    def init_hardware(self):
        # Configure the detector's gpio pin
        self.m_pin = Pin(self.m_gpio_pin, Pin.IN, self.m_gpio_pull_pin)
        owner = self.ident()
        self.m_pin = GPIO.GPIO(owner, self.m_gpio_pin, Pin.IN, self.m_gpio_pull_pin)
        if self.m_pin is None:
            return False

        # Setup interrupt handler to monitor the gpio pin
        trigger = Pin.IRQ_FALLING | Pin.IRQ_RISING
        priority = 1
        wake = machine.IDLE | machine.SLEEP | machine.DEEPSLEEP
        hard = False
        try:
            self.m_pin.irq(gpio_pin_callback, trigger, priority, wake, hard)
        except ValueError:
            msg = "gpio pin does not support callback: "
            msg += self.m_gpio_pin
            msg += " 202411211500"
            p_log.add("Detector", msg)
            return False

        return True


    # Call by the interrupt handler whenever the detector gpio pin changes state
    #
    def change_state_interrupt(self):


# Interrupt callback triggered by change in the level on the gpio pin
# @param p_pin The Pin value of the gpio causing the interrupt
#
def gpio_pin_callback(p_pin):
    Detector.PinChangeState(p_pin)


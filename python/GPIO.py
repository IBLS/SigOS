#
# Registration service for GPIO pins.  Prevents duplicate use of gpio pins.
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
import machine
from machine import Pin

# See Characterizing GPIO input pins - https://forums.raspberrypi.com/viewtopic.php?t=133740

class GPIO:

    # Hold the list of all registered GPIO objects
    c_gpio_list = list()


    # Create a new instance of this class
    # @param p_owner The name of the owner (if the pin is not already aquired)
    # @param p_id The identifier of the gpio pin (integer pin number or string pin name)
    # @param p_mode The pin mode of operation (e.g. Pin.IN, Pin.OUT, etc)
    # @param p_pull Specifies pull-up or pull-down resistor (e.g. None, Pin.PULL_UP, Pin.PULL_DOWN)
    # @param p_log The log object to report messages through
    # @returns The initialized pin, None if the configuration is not valid for the current hardware
    #
    def __init__(self, p_owner, p_id, p_mode, p_pull, p_log):

        # Make sure the gpio pin has not already been acquired
        for gpio in GPIO.c_gpio_list:
            if gpio.m_id == p_id:
                msg = "Pin("
                msg += p_id
                msg += ") requested by "
                msg += p_owner
                msg += " already owned by "
                msg += gpio.m_owner
                msg += " 202411211454"
                p_log.add("GPIO", msg)

        self.m_owner = p_owner
        self.m_id = p_id
        self.m_mode = p_mode
        self.m_pull = p_pull
        self.m_pin = None

        try:
            # Try to configure the specified pin, will throw exception if
            # this is not a valid configuration for the hardware.
            self.m_pin = Pin(p_id, self.m_mode)
        except ValueError:
            msg = "Invalid gpio pin number, mode or pull-up: "
            msg += p_id
            msg += " 202411210243"
            p_log.add("GPIO", msg)

        # Add to my list and return
        GPIO.c_gpio_list.append(self)


    # @returns A string representation of this GPIO
    #
    def __str__(self):
        s = "GPIO owner:"
        s += str(self.m_owner)
        s += ", id:"
        s += str(self.m_id)
        s += ", mode:"
        s += str(self.m_mode)
        s += ", pull:"
        s += str(self.m_pull)
        return s



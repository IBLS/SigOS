#
# Defines Hardware interfaces for SigOS
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

# Nomenclature: B, B-, B+
# B means the block protected by the semaphore
# B- means the block immediately preceeding the protected block B
# B+ means the block immediately following the protected block B
# This nomenclature is in respect to the direction of the train
# moving from B- into B and viewing the semaphore's face

import sys
import machine
from machine import Pin, PWM
import ubinascii
import Semaphore
import Light
import WS281

class Hardware:

    # Class variable that holds the singleton instance of Hardware
    c_hardware = None

    # This will hoold the WS281 singleton controller object
    c_ws281 = None

    # Determine underlying hardware and initialize pins
    #
    def __init__(self):
        self.m_platform = sys.platform
        self.m_unique_id = ubinascii.hexlify(machine.unique_id())

        if (self.m_platform == 'esp8266'):
            # ESP8266 pinout
            # Pin 1 - GND
            # Pin 2 - On-board LED and WS281 for lights/LED
            # Pin 3 - Detect B
            # Pin 4 - Detect B-
            # Pin 5 - Servo control out - GND at power-on to program
            # Pin 6 - /Reset (unused)
            # Pin 7 - Detect B+
            # Pin 8 - VCC
            self.m_detect_b  = Pin(3, Pin.IN, Pin.PULL_UP)
            self.m_detect_bm = Pin(4, Pin.IN, Pin.PULL_UP)
            self.m_detect_bp = Pin(7, Pin.IN, Pin.PULL_UP)
        elif (self.m_platform == "esp32"):
            # ESP32 S2 mini pins used - tries to use same "pin" numbers as ESP8266
            # Pin 2 - LED light
            # Pin 3 - detect block B
            # Pin 4 - detect block B-
            # Pin 5 - Servo control out
            # Pin 7 - detect block B+
            self.m_detect_b  = Pin(3, Pin.IN, Pin.PULL_UP)
            self.m_detect_bm = Pin(4, Pin.IN, Pin.PULL_UP)
            self.m_detect_bp = Pin(7, Pin.IN, Pin.PULL_UP)
        else:
            raise Exception('Unrecognized hardware {} 02407241136', self.m_platform)

        # All semaphores live here
        self.m_semaphore_list = list()

        # All lights live here
        self.m_light_list = list()

        # Placeholder for the WS281 hardware control object
        Hardware.c_ws281 = None

        # Save this singleton instance
        Hardware.c_hardware = self


    # Initialize all Hardware as needed. Call this method after
    # loading all Config but before executing Rules that change Aspects.
    # @param p_config The configuration object
    #
    @classmethod
    def InitHardware(p_class, p_config):
        Hardware.c_ws281 = WS281.WS281(p_config.m_ws281_gpio_pin, Hardware.LightCount(), p_config.m_color_chart)
        Hardware.c_ws281.all_off()

        for semaphore in p_class.c_hardware.m_semaphore_list:
            semaphore.init_hardware()

        for light in p_class.c_hardware.m_light_list:
            light.init_hardware()


    # Add a Semaphore object
    # @param p_semaphore The Semaphore to add
    #
    @classmethod
    def AddSemaphore(p_class, p_semaphore):
        p_class.c_hardware.m_semaphore_list.append(p_semaphore)


    # Modify the aspect of the specified semaphore
    # @param p_head_id Specifies the head containing the semaphore
    # @param p_angle The new angle for the semaphore flag
    # @param p_log Log to write failure messages to
    # @returns True on success, False on error
    #
    @classmethod
    def ChangeSemaphoreAspect(p_class, p_head_id, p_angle, p_log):
        for semaphore in p_class.c_hardware.m_semaphore_list:
            if p_head_id == semaphore.m_head_id:
                # change the aspect
                semaphore.set_aspect(p_angle)
                return True
        p_log.add("Hardware", "No matching Semaphore 202410160900")
        return False


    # Add a Light object
    # @param p_light The Light to add
    #
    @classmethod
    def AddLight(p_class, p_light):
        p_class.c_hardware.m_light_list.append(p_light)


    # Modify the aspect of the specified light
    # @param p_head_id Specifies the head containing the light
    # @param p_color The new color for the light
    # @param p_intensity The new intensity for the light (0-100)
    # @param p_flashing To flash or not to flash, that is the question
    # @param p_log Log to write failure messages to
    # @returns True on success, False on error
    #
    @classmethod
    def ChangeLightAspect(p_class, p_head_id, p_color, p_intensity, p_flashing, p_log):
        for light in p_class.c_hardware.m_light_list:
            if p_head_id == light.m_head_id:
                if p_color in light.m_color_list:
                    # change the aspect
                    return light.set_aspect(Hardware.c_ws281, p_color, p_intensity, p_flashing, p_log)
        p_log.add("Hardware", "No matching light 202410160901")
        return False


    # @returns The number of registered semaphores from Config
    #
    @classmethod
    def SemaphoreCount(p_class):
        return len(p_class.c_hardware.m_semaphore_list)


    # @returns The number of registered lights from Config
    #
    @classmethod
    def LightCount(p_class):
        return len(p_class.c_hardware.m_light_list)


    # @returns True if the B input signal has detected a train
    #
    def get_detect_b(self):
        return self.m_detect_b.value()


    # @returns True if the B- input signal has detected a train
    #
    def get_detect_bm(self):
        return self.m_detect_bm.value()


    # @returns True if the B+ input signal has detected a train
    #
    def get_detect_bp(self):
        return self.m_detect_bp.value()


#
# Class for modeling a Light in SigOS
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
from machine import Pin, PWM, Timer
import WS281


class Light:

    # Store each created Light in this class list
    c_light_list = list()

    # Class variable for generating timer id's
    c_timer_id = 1

    # Create a Light object
    # @param p_head_id The identifier (number) of the Head containing this light,
    #                  1 is the highest head, 2 is the next highest, etc
    # @param p_light_id The identifier (number) of the Light, 1 is highest on the head,
    #             2 is next highest, etc
    # @param p_ws281_id The zero-based index of the LED in the WS281 chain
    # @param p_flashes_per_minute The number of times to flash in 60 seconds
    # @param p_color_list A list of one or more valid color names for this light
    #
    def __init__(self, p_head_id, p_light_id, p_ws281_id, p_flashes_per_minute, p_color_list):
        self.m_head_id = p_head_id
        self.m_light_id = p_light_id
        self.m_ws281_id = p_ws281_id
        self.m_flashes_per_minute = p_flashes_per_minute
        self.m_color_list = p_color_list
        self.m_inhibit_req = False
        self.m_update_ack = False
        self.m_timer = None
        # Stores current Aspect settings
        self.m_ws281 = None
        self.m_aspect_color = None
        self.m_aspect_intensity = None
        self.m_aspect_flashing = False
        self.m_aspect_flashing_on = False
        self.m_log = None

        # Save the new instance in the class
        Light.c_light_list.append(self)


    # Destructor
    #
    def __del__(self):
        if self.m_timer:
            self.m_timer.deinit()


    # Initialize the hardware associated with Lights, if any.
    # Call this method after loading all Config but before executing Rules that change Aspects.
    # @param p_config The configuration object
    #
    @classmethod
    def InitHardware(p_class, p_config):
        for light in p_class.c_light_list:
            light.init_hardware()


    # @returns The number of created Light objects
    #
    @classmethod
    def Count(p_class):
        return len(p_class.c_light_list)


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
        for light in p_class.c_light_list:
            if p_head_id == light.m_head_id:
                if p_color in light.m_color_list:
                    # change the aspect
                    return light.set_aspect(WS281.WS281.c_ws281, p_color, p_intensity, p_flashing, p_log)
        p_log.add("Light", "No matching light 202410160901")
        return False


    # Toggle lights with Aspect of "flashing"
    #
    @classmethod
    def AdjustFlash(p_class):
        for light in p_class.c_light_list:
            light.adjust_flash()



    # This method will inhibit the output of a light.  Typically called by a
    # Semaphore during movement.
    # @param p_head_id The head-id of the light to inhibit
    # @param p_inhibit The inhibit state, True for inhibit
    #
    @classmethod
    def Inhibit(p_class, p_head_id, p_inhibit):
        for light in p_class.c_light_list:
            if p_head_id == light.m_head_id:
                # Found the matching light
                # Change inhibit state
                light.m_inhibit_req = p_inhibit
                light.m_update_ack = False


    # Initialize Light hardware
    # Note: this is performed in the WS281 driver
    #
    def init_hardware(self):
        # Start timer
        self.m_timer = machine.Timer(Light.c_timer_id)
        # Compute the timer interrupt period.
        period = 60.0 / self.m_flashes_per_minute
        # Halve the period, because we need two interrupts per flash (on then off).
        period /= 2.0
        # Convert from seconds to milliseconds
        i_period = int(period * 1000.0)
        if i_period <= 0:
            msg = "Invalid value for flashes-per-minute ("
            msg += str(self.m_flashes_per_minute)
            msg += ") 202410170833"
            self.m_log.add("Light", msg)
            return
        self.m_timer.init(mode=Timer.PERIODIC, period=i_period, callback=flashing_callback)


    # Modify the aspect of this light
    # @param p_ws281 The singleton hardware object controlling the WS281 hardware
    # @param p_color The name of the color to set.
    # @param p_intensity The brightness of the light in % (0-100)
    # @param p_flashing When True then make this light flash
    # @param p_log Log to write error messages to
    # @returns True on success, False if the requested state does not match
    #
    def set_aspect(self, p_ws281, p_color, p_intensity, p_flashing, p_log):
        self.m_ws281 = p_ws281
        self.m_aspect_color = p_color
        self.m_aspect_intensity = p_intensity
        self.m_aspect_flashing = p_flashing
        self.m_aspect_flashing_on = p_flashing
        self.m_log = p_log
        self.m_update_ack = False
        # All LED updates are performed in the timer callback adjust_flash()
        return True


    # Called by timer handler to toggle lights with Aspect of flashing
    #
    def adjust_flash(self):
        if not self.m_ws281:
            return

        if self.m_log:
            self.m_log.add("adjust_flash", "inhibit_req:" + str(self.m_inhibit_req))

        if not self.m_update_ack and self.m_inhibit_req:
            self.m_update_ack = True
            self.m_ws281.set_color(self.m_ws281_id, "off", self.m_aspect_intensity, self.m_log)
            return

        if not self.m_update_ack and not self.m_inhibit_req:
            self.m_update_ack = True
            self.m_ws281.set_color(self.m_ws281_id, self.m_aspect_color, self.m_aspect_intensity, self.m_log)
            return

        # Prevent flashing while the LED is inhibited
        if self.m_inhibit_req:
            return

        if self.m_aspect_flashing and self.m_aspect_flashing_on:
            self.m_aspect_flashing_on = False
            self.m_ws281.set_color(self.m_ws281_id, "off", self.m_aspect_intensity, self.m_log)
            return

        if self.m_aspect_flashing and not self.m_aspect_flashing_on:
            self.m_aspect_flashing_on = True
            self.m_ws281.set_color(self.m_ws281_id, self.m_aspect_color, self.m_aspect_intensity, self.m_log)
            return


    # @returns A string representation of this Light
    #
    def __str__(self):
        s = "  light: "
        s += str(self.m_light_id)
        s += "\n    head-id: "
        s += str(self.m_head_id)
        s += "\n    colors: "
        s += str(self.m_colors)
        return s


# Timer callback to toggle lights with Aspect of flashing
#
def flashing_callback(p_timer):
    Light.AdjustFlash()



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
    # @param p_log The Log file to print messages to.
    #
    def __init__(self, p_head_id, p_light_id, p_ws281_id, p_flashes_per_minute, p_color_list, p_log):
        self.m_head_id = p_head_id
        self.m_light_id = p_light_id
        self.m_ws281 = None
        self.m_ws281_id = p_ws281_id
        self.m_flashes_per_minute = p_flashes_per_minute
        self.m_color_list = p_color_list
        self.m_state_on = False
        self.m_inhibit = False
        self.m_update_req = False
        self.m_timer = None
        self.m_aspect_color = None
        self.m_aspect_intensity = 100
        self.m_aspect_flashing = False
        self.m_log = p_log

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


    # Check the Light list for one that matches the input parameters
    # @param p_head_id The Head ID of the Light to match
    # @returns The matching Light, or None
    #
    @classmethod
    def CheckForMatch(p_class, p_head_id, p_color):
        for light in p_class.c_light_list:
            if p_head_id == light.m_head_id:
                if p_color in light.m_color_list:
                    return light
        return None


    # Toggle lights with Aspect of "flashing"
    #
    @classmethod
    def AdjustFlash(p_class):
        for light in p_class.c_light_list:
            light.adjust_flash()


    # Toggle lights with Aspect of "flashing"
    # @param p_intensity_percent The intensity as a percentage 0-100
    #
    @classmethod
    def AdjustIntensity(p_class, p_intensity_percent):
        for light in p_class.c_light_list:
            light.adjust_intensity(p_intensity_percent)


    # Turn all lights off. Called before changing Aspects
    #
    @classmethod
    def AllOff(p_class):
        for light in p_class.c_light_list:
            light.off()


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
                light.m_inhibit = p_inhibit


    # Initialize Light hardware
    # Note: this is performed in the WS281 driver
    #
    def init_hardware(self):
        # Save link to WS281 driver
        self.m_ws281 = WS281.WS281.c_ws281
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
    # @param p_color The name of the color to set.
    # @param p_flashing When True then make this light flash
    # @returns True on success, False if the requested state does not match
    #
    def set_aspect(self, p_color, p_flashing):
        self.m_aspect_color = p_color
        self.m_aspect_flashing = p_flashing
        self.m_state_on = True
        self.m_update_req = True
        # All LED updates are performed in the timer callback adjust_flash()
        return True


    # Turn this light off
    #
    def off(self):
        self.set_aspect("black", False)


    # Called by timer handler to toggle lights with Aspect of flashing
    #
    def adjust_flash(self):
        if self.m_inhibit:
            # Turn off LED - this is the highest priority action
            self.m_ws281.set_color(self.m_ws281_id, "black", self.m_aspect_intensity, self.m_log)
            return

        if self.m_aspect_flashing:
            # Update flashing on every interrupt
            self.m_update_req = True

        if not self.m_update_req:
            # Nobody has requested an update
            return

        if self.m_state_on:
            self.m_ws281.set_color(self.m_ws281_id, self.m_aspect_color, self.m_aspect_intensity, self.m_log)
        else:
            self.m_ws281.set_color(self.m_ws281_id, "black", self.m_aspect_intensity, self.m_log)

        # Update flashing state for next interrupt
        if self.m_aspect_flashing:
            if self.m_state_on:
                self.m_state_on = False
            else:
                self.m_state_on = True

        # Acknowledge the update has occured
        self.m_update_req = False


    # Called by timer handler to toggle lights with Aspect of flashing
    # @param p_intensity_percent The intensity as a percentage 0-100
    #
    def adjust_intensity(self, p_intensity_percent):
        self.m_aspect_intensity = int(p_intensity_percent)
        # Change intensity
        self.m_update_req = True
        #self.adjust_flash()


    # @returns A string representation of this Light
    #
    def __str__(self):
        s = "light:"
        s += str(self.m_light_id)
        s += ", head-id:"
        s += str(self.m_head_id)
        s += ", colors:"
        s += str(self.m_color_list)
        s += ", ws281-id:"
        s += str(self.m_ws281_id)
        s += ", flashes-per-minute:"
        s += str(self.m_flashes_per_minute)
        s += ", state_on:"
        s += str(self.m_state_on)
        s += ", inhibit:"
        s += str(self.m_inhibit)
        s += ", aspect_color:"
        s += str(self.m_aspect_color)
        s += ", aspect_intensity:"
        s += str(self.m_aspect_intensity)
        s += ", aspect_flashing:"
        s += str(self.m_aspect_flashing)
        return s


# Timer callback to toggle lights with Aspect of flashing
#
def flashing_callback(p_timer):
    Light.AdjustFlash()



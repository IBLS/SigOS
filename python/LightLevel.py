#
# Class to monitor the Light Level Sensor
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
from machine import ADC, Pin, Timer
import Light
import Config


class LightLevel:

    # Holds the LightLevel singleton
    c_light_level = None

    # Class variable for generating timer id's
    c_timer_id = 1

    # Create the singleton object for monitoring the ambient light level.
    #
    def __init__(self):
        self.m_light_level_percent = None
        self.m_light_level_gpio_pin = None
        self.m_light_level_min_percent = None
        self.m_light_level_max_percent = None
        self.m_adc = None
        self.m_adc_uv_max = 0
        self.m_timer = None
        LightLevel.c_light_level = self


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
        LightLevel()
        p_class.c_light_level.init_hardware(p_config)


    # Initialize ambient light level hardware.
    # @param p_config The configuration object
    #
    def init_hardware(self, p_config):
        # Get config values
        self.m_light_level_percent = p_config.get_value("light-level-percent")
        self.m_light_level_pin = p_config.get_value("light-level-gpio-pin")
        self.m_light_level_min_percent = p_config.get_value("light-level-min-percent")
        self.m_light_level_max_percent = p_config.get_value("light-level-max-percent")

        if (self.m_light_level_percent != "auto"):
            # Set light level to constant percentage
            Light.Light.AdjustIntensity(self.m_light_level_percent)
            return

        # Setup the A/D converter
        self.m_adc = ADC(Pin(self.m_light_level_pin))
        # Set 11dB attenuation (150mV - 2450mV)
        self.m_adc.atten(ADC.ATTN_11DB)
        # This is the resulting value from read_uv() with max input
        self.m_adc_uv_max = 2667000

        # Start timer
        self.m_timer = machine.Timer(LightLevel.c_timer_id)
        # Set timer for 1 second interrupt period
        period = 1.0
        # Convert from seconds to milliseconds
        i_period = int(period * 1000.0)
        self.m_timer.init(mode=Timer.PERIODIC, period=i_period, callback=light_level_callback)


    # Read the current ambient light level and adjust the output Light levels
    #
    def read_light_level(self):
        # Read the current microvolts and convert to percentage
        uv = self.m_adc.read_uv()
        percent_intensity = (uv * 100) / self.m_adc_uv_max

        # Keep within the configured min/max levels
        if percent_intensity < self.m_light_level_min_percent:
            percent_intensity = self.m_light_level_min_percent
        elif percent_intensity > self.m_light_level_max_percent:
            percent_intensity = self.m_light_level_max_percent

        Light.Light.AdjustIntensity(percent_intensity)


# Timer callback to read ambient light level and adjust Light output levels
#
def light_level_callback(p_timer):
    LightLevel.c_light_level.read_light_level()


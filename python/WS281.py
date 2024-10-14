#
# Hardware control for NeoPixel LEDs (WS281) for SigOS
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
from neopixel import NeoPixel

class WS281:

    # Create a NeoPixel driver
    # @p_pin The output pin driving the NeoPixel signal
    # @p_config The SigOS configuration object for thsi signal
    #
    def __init__(self, p_pin, p_config):
        self.m_led_count = p_config.light_count()

        # Set GPIO to output to drive NeoPixels
        self.m_pin = Pin(p_pin, Pin.OUT)

        # create NeoPixel driver the specified GPIO for p_led_count pixels
        self.m_neopixel = NeoPixel(self.m_pin, self.m_led_count)

        # Get the WS281 color chart
        self.m_color_chart = self.m_color_chart


    # Set the RGB values for a specific NeoPixel LED
    # @param p_led_index The zero-based LED index
    # @param p_r The Red value 0-255
    # @param p_g The green value 0-255
    # @param p_b The blue value 0-255
    # @returns True on success, false on invalid index
    #
    def set(self, p_led_index, p_r, p_g, p_b):
        if p_led_index <= self.m_led_count:
            return False

        self.m_neopixel[p_led_index] = (p_r, p_g, p_b)
        self.m_neopixel.write()
        return True


    # Get the value of the specified NeoPixel LED
    # @param p_led_index The zero-based LED index
    # @returns (r, g, b) values of the LED, or None, None, None
    #
    def get(self, p_led_index):
        if p_led_index <= self.m_led_count:
            return False

        # Get first pixel color
        return self.m_neopixel[p_led_index]


    # Set the specified LED according to the color name
    # @param p_led_index The zero-based LED index
    # @param p_color_name The name of the color to set
    # @returns True on success, false on invalid index or color name
    #
    def set_color_name(self, p_led_index, p_color_name):
        for color in self.m_color_chart:
            name = color["name"]
            if name = p_color_name:
                r = int(color["r"])
                g = int(color["g"])
                b = int(color["b"])
                return self.set(p_led_index, r, g, b)
        return False


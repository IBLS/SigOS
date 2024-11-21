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
import Config
import GPIO


class WS281:

    # Create a NeoPixel driver on a specific GPIO pin
    # @p_pin The output pin driving the NeoPixel signal
    # @p_light_count Number of lights driven on this chaing
    # @p_color_char The color chart from Config
    # @param p_log The logger object for error messages
    #
    def __init__(self, p_pin, p_light_count, p_color_chart, p_log):
        self.m_led_count = p_light_count

        # Set GPIO to output to drive NeoPixels
        self.m_gpio = GPIO.GPIO("WS281", p_pin, Pin.OUT, None, p_log)

        # create NeoPixel driver the specified GPIO for p_led_count pixels
        self.m_neopixel = NeoPixel(self.m_gpio.m_pin, self.m_led_count)

        # Get the WS281 color chart
        self.m_color_chart = p_color_chart

        self.all_off()


    # Destructor - shut down PWM
    #
    def __del__(self):
        self.all_off()
        self.m_neopixel.deinit()


    # Initialize all Hardware as needed. Call this method after
    # loading all Config but before executing Rules that change Aspects.
    # @param p_config The configuration object
    # @param p_light_count Total number of WS281 lights on the chain.
    # @param p_log The logger object for error messages
    #
    @classmethod
    def InitHardware(p_class, p_config, p_light_count, p_log):
        WS281.c_ws281 = WS281(p_config.m_ws281_gpio_pin, p_light_count, p_config.m_color_chart, p_log)
        WS281.c_ws281.all_off()


    # Turn off all LEDs
    #
    def all_off(self):
        # Turn off all LEDs
        for i in range(self.m_led_count):
            self.set(i, 0, 0, 0)


    # Set the RGB values for a specific NeoPixel LED
    # @param p_led_index The zero-based LED index
    # @param p_r The Red value 0-255
    # @param p_g The green value 0-255
    # @param p_b The blue value 0-255
    # @returns True on success, false on invalid index
    #
    def set(self, p_led_index, p_r, p_g, p_b):
        if p_led_index >= self.m_led_count:
            return False

        self.m_neopixel[p_led_index] = (int(p_r), int(p_g), int(p_b))
        self.m_neopixel.write()
        return True


    # Get the value of the specified NeoPixel LED
    # @param p_led_index The zero-based LED index
    # @returns (r, g, b) values of the LED, or None, None, None
    #
    def get(self, p_led_index):
        if p_led_index >= self.m_led_count:
            return False

        # Get first pixel color
        return self.m_neopixel[p_led_index]


    # Set the specified LED according to the color name
    # @param p_led_index The zero-based LED index
    # @param p_color_name The name of the color to set
    # @param p_intensity Brightness of the color as a percentage, 0% to 100%
    # @param p_log Log to write errors to
    # @returns True on success, false on invalid index or color name
    #
    def set_color(self, p_led_index, p_color_name, p_intensity, p_log):
        for color in self.m_color_chart:
            if color["name"] == p_color_name:
                r = int(color["r"])
                g = int(color["g"])
                b = int(color["b"])
                if (p_intensity < 100):
                    r = (r * p_intensity) / 100
                    g = (g * p_intensity) / 100
                    b = (b * p_intensity) / 100
                return self.set(p_led_index, r, g, b)
        p_log.add("WS281", "No matching color in chart 202410160905")
        return False


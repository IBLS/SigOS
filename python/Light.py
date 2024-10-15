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

import WS281


class Light:

    # Create a Light object
    # @param p_head_id The identifier (number) of the Head containing this light,
    #                  1 is the highest head, 2 is the next highest, etc
    # @param p_light_id The identifier (number) of the Light, 1 is highest on the head,
    #             2 is next highest, etc
    # @param p_flashes_per_minute The number of times to flash in 60 seconds
    # @param p_color_list A list of one or more valid color names for this light
    #
    def __init__(self, p_head_id, p_light_id, p_flashes_per_minute, p_color_list):
        self.m_head_id = p_head_id
        self.m_light_id = p_light_id
        self.m_flashes_per_minute = p_flashes_per_minute
        self.m_color_list = p_color_list


    # Initialize Light hardware
    # Note: this is performed in the WS281 driver
    #
    def init_hardware(self):
        pass


    # Modify the aspect of this light
    # @param p_ws281 The singleton hardware object controlling the WS281 hardware
    # @param p_color The name of the color to set.
    # @param p_intensity The brightness of the light in % (0-100)
    # @param p_flashing When True then make this light flash
    # @returns True on success, False if the requested state does not match
    #
    def set_aspect(self, p_ws281, p_color, p_intensity, p_flashing):
        for color in self.m_color_list:
            if p_color == color:
                # Make the change
                return p_ws281.set_color(p_color, p_intensity, p_flashing)
        return False


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


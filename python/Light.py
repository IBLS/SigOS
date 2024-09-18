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

class Light:

    # Create a Light object
    # @param p_head_id The identifier (number) of the Head containing this light,
    #                  1 is the highest head, 2 is the next highest, etc
    # @param p_light_id The identifier (number) of the Light, 1 is highest on the head,
    #             2 is next highest, etc
    # @param p_colors A list of one or more valid color names for this light
    #
    def __init__(self, p_head_id, p_light_id, p_colors):
        self.m_head_id = p_head_id
        self.m_light_id = p_light_id
        self.m_colors = p_colors


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


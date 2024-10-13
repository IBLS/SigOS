#
# Class for performing Actions for Rules
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

class Action:

    def __init__(self):
        self.m_head = None

        self.m_semaphore = False
        self.m_angle = 0

        self.m_light = False
        self.m_color = None
        self.m_flashing = False

        self.number_plate = False


    # @returns A string representation of this object
    #
    def __str__(self):
        s = "head:"
        s += self.m_head
        s += ",semaphore:"
        s += self.m_semaphrore
        s += ",angle:"
        s += self.m_angle
        s += ",color:"
        s += self.m_color
        s += ",light:"
        s += self.m_light
        s += ",color:"
        s += self.m_color
        s += ",flashing:"
        s += self.m_flashing
        return s


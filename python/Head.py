#
# Class for encapsulating a signal head for SigOS
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

import Semaphore
import Light

class Head:

    # Create a Rule object to encapsulates a single operating rule
    # @param p_head_id ID of the head
    #
    def __init__(self, p_head_id):
        self.m_head_id = p_head_id
        self.m_light_list = list()
        self.m_semaphore_list = list()


    # Add a light to this signal head
    # @param p_light_obj A Light object
    #
    def add_light(self, p_light_obj):
        self.m_light_list.append(p_light_obj)


    # Add a semaphore to this signal head.
    # @param p_semaphore_obj An Semaphore object
    #
    def add_semaphore(self, p_semaphore_obj):
        self.m_semaphore_list.append(p_semaphore_obj)


    # @returns The number of lights on this head
    #
    def light_count(self):
        return len(self.m_light_list)


    # @returns The number of semaphores on this head
    #
    def semaphore_count(self):
        return len(self.m_semaphore_list)


    # @returns A string representation of this head
    #
    def __str__(self):
        s = "  head_id: "
        s += str(self.m_head_id)

        for light in self.m_light_list:
            s += str(light)

        for semaphore in self.m_semaphore_list:
            s += str(semaphore)

        s += "\n"
        return s


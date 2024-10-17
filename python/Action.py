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

import Semaphore
import Light
import Log


class Action:

    def __init__(self):
        self.m_head_id = None

        self.m_semaphore = False
        self.m_angle = None

        self.m_light = False
        self.m_color = None
        self.m_intensity = 100
        self.m_flashing = False


    # Validate the values assigned to this action
    # @param p_source The source requesting the execution
    # @param p_log Log to print error messages
    # @returns True on valid test
    #
    def validate(self, p_source, p_log):
        if self.m_semaphore:
            if self.m_angle >= 0 and self.m_angle <= 90:
                return True
        elif self.m_light:
            if not self.m_color:
                p_log.add("Action", "Invalid color 202410151804")
                return False
            if self.m_intensity >= 0 and self.m_intensity <= 100:
                return True
        else:
            p_log.add("Action", "Validate failed 202410160833")
            return False


    # Execute this Action
    # @param p_source The source requesting the execution
    # @param p_log Log to print error messages
    # @returns True on success, False on failure
    #
    def execute(self, p_source, p_log):
        if not self.validate(p_source, p_log):
            return False

        if self.m_semaphore:
            return Semaphore.Semaphore.ChangeSemaphoreAspect(self.m_head_id, self.m_angle, p_log)

        if self.m_light:
            return Light.Light.ChangeLightAspect(self.m_head_id, self.m_color, self.m_intensity, self.m_flashing, p_log)

        p_log.add("Action", "Invalid fixture 202410160829")
        return False


    # @returns A string representation of this object
    #
    def __str__(self):
        s = "head_id:"
        s += str(self.m_head_id)
        s += ",semaphore:"
        s += str(self.m_semaphore)
        s += ",angle:"
        s += str(self.m_angle)
        s += ",light:"
        s += str(self.m_light)
        s += ",color:"
        s += self.m_color
        s += ",intensity:"
        s += str(self.m_intensity)
        s += ",flashing:"
        s += str(self.m_flashing)
        return s


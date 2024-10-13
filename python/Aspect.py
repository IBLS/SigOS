#
# Class for managing the Aspect of a Rule
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

import Config
import Action

class Aspect:

    # Create a new Aspect
    # @param p_aspect_commands A string of aspect commands
    #
    def __init__(self, p_aspect_commands):
        self.m_config = Config.Config.c_config

        # Make parsing easier by converting to lower case
        self.m_aspect_commands = p_aspect_commands.lower()
        self.m_action_list = list()

        # Criteria that must match Config
        self.m_head_count = 0
        self.m_semaphore_count = 0
        self.m_light_count = 0
        self.m_number_plate = None

        self.m_valid_config = False

        # Create a log object for convenience
        self.m_log = Log.Log()


    # Evaluate the aspect string. Save the condition results,
    # but do not execute the actions.
    # @returns True on success, False on evaluation error
    #
    def eval(self):
        aspect_cmds = self.m_aspect_commands.split(';')
        for aspect_cmd in aspect_cmds:
            if not self.eval_single_aspect(aspect_cmd):
                return False

        self.m_valid_config = self.check_config()
        return m_valid_config

    # Evaluate a single aspect command>
    # @p_aspect_cmd An aspect command string.
    # @returns True on success, false on parsing error
    #
    def eval_single_aspect(self, p_aspect_cmd):
        # Keywords to collect in this parser
        fixture = None
        head = None
        angle = None
        color = None
        flashing = False

        words = p_aspect_cmd.split()
        for word in words:
            # Split arguments, if any
            args = word.split(':')

            # Look for fixture names first
            if args[0] == "semaphore":
                fixture = word
                continue

            if args[0] == "light":
                fixture = word
                continue

            if args[0] == "number-plate":
                if args[1] == "yes":
                    self.m_number_plate = True
                if args[1] == "no":
                    self.m_number_plate = False
                continue

            if args[0] == "head":
                head = int(arg[1])
                continue

            if args[0] == "angle":
                angle = int(arg[1])
                continue

            if args[0] == "color":
                color = arg[1]
                continue

            if args[0] == "flashing":
                flashing = True
                continue

        # Create an action
        if fixture == "semaphore":
            if not head:
                self.m_log.add(self.m_config.m_hostname, \
                    "Missing head parameter 202410112052");
                return False
            if not angle:
                self.m_log.add(self.m_config.m_hostname, \
                    "Missing angle parameter 202410112053");
                return False;
            action = Action.Action()
            action.m_semaphore = True
            action.m_head = head
            action.m_angle = angle
            action.m_number_plate = self.m_number_plate
            self.m_action_list.append(action)
            self.m_head_count += 1
            self.m_semaphore_count +=1 

        elif fixture == "light":
            if not head:
                self.m_log.add(self.m_config.m_hostname, \
                    "Missing head parameter 202410112054");
                return False
            if not color:
                self.m_log.add(self.m_config.m_hostname, \
                    "Missing color parameter 202410112056");
                return False
            action = Action.Action()
            action.m_light = True
            action.m_color = color
            action.m_flashing = flashing
            action.m_number_plate = self.m_number_plate
            self.m_action_list.append(action)
            self.m_head_count += 1
            self.m_light_count += 1
        else:
            self.m_log.add(self.m_config.m_hostname, \
                "Invalid aspect 202410112057");
            return False

        return True


    # Check this Aspect again the Configuration of this signal.
    # Determine if this Aspect is approrpirate for this Config.
    # @returns True if this Aspect matches the Config, False otherwise
    #
    def check_config(self):
        if self.m_head_count != self.m_config.head_count():
            return False

        if self.m_semaphore_count != self.m_config.semaphore_count():
            return False

        if self.m_light_count != self.m_config.light_count():
            return False

        # Only check for a number plate if it was specifically defined
        # in this Aspect.
        if self.m_number_plate is not None:
            if self.m_number_plate != self.m_config.number_plate():
                return False

        # This Aspect matches the Configuration
        return True



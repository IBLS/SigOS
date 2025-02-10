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
import Semaphore
import Light
import Log

class Aspect:

    # Create a new Aspect
    # @param p_aspect_commands A string of aspect commands
    # @param p_config Reference to the Config object
    # @param p_log Reference to the Log object
    #
    def __init__(self, p_aspect_commands, p_config, p_log):
        self.m_log = p_log
        self.m_config = p_config

        # Make parsing easier by converting to lower case
        self.m_aspect_commands = p_aspect_commands.lower()
        self.m_action_list = list()

        # Criteria that must match Config
        self.m_head_list = list()
        self.m_number_plate = None

        self.m_valid_config = False


    # Evaluate the aspect string. Save the condition results,
    # but do not execute the actions.
    # @returns True on success, False on evaluation error
    #
    def eval(self):
        aspect_cmds = self.m_aspect_commands.split(';')
        for aspect_cmd in aspect_cmds:
            if not self.eval_single_aspect(aspect_cmd):
                # This Aspect is invalid for the current configuration
                return False

        # Perform a check on the command results
        self.m_valid_config = self.check_config()
        return self.m_valid_config


    # Evaluate a single aspect command>
    # @p_aspect_cmd An aspect command string.
    # @returns True on success, false on parsing error
    #
    def eval_single_aspect(self, p_aspect_cmd):
        # Keywords to collect in this parser
        fixture = None
        number_plate = None
        head_id = None
        angle = None
        color = None
        flashing = False

        words = p_aspect_cmd.split()
        for word in words:
            # Split arguments, if any
            args = word.split(':')

            # Look for fixture names first
            if args[0] == "semaphore":
                fixture = args[0]
                continue

            if args[0] == "light":
                fixture = args[0]
                continue

            if args[0] == "number-plate":
                fixture = args[0]
                continue

            if args[0] == "present":
                if args[1] and args[1] == "yes":
                    number_plate = True
                else:
                    number_plate = False
                continue

            if args[0] == "head-id":
                head_id = int(args[1])
                continue

            if args[0] == "angle":
                angle = int(args[1])
                continue

            if args[0] == "color":
                color = args[1]
                continue

            if args[0] == "flashing":
                flashing = True
                continue

        # Create an action
        if fixture == "semaphore":
            if not head_id:
                self.m_log.add(self.m_config.m_hostname, p_aspect_cmd)
                self.m_log.add(self.m_config.m_hostname, \
                    "Missing head parameter 202410112052");
                return False
            if not isinstance(angle, int):
                self.m_log.add(self.m_config.m_hostname, p_aspect_cmd)
                self.m_log.add(self.m_config.m_hostname, \
                    "Missing angle parameter 202410112053");
                return False
            matching_semaphore = Semaphore.Semaphore.CheckForMatch(head_id)
            if not matching_semaphore:
                # No semaphore matching this description in the config file
                #print("No semaphore:", head_id)
                return False
            action = Action.Action()
            action.m_head_id = head_id
            action.m_semaphore = matching_semaphore
            action.m_angle = angle
            self.m_action_list.append(action)
            if head_id not in self.m_head_list:
                self.m_head_list.append(head_id)
            return True

        if fixture == "light":
            if not head_id:
                self.m_log.add(self.m_config.m_hostname, p_aspect_cmd)
                self.m_log.add(self.m_config.m_hostname, \
                    "Missing head parameter 202410112054");
                return False
            if not color:
                self.m_log.add(self.m_config.m_hostname, p_aspect_cmd)
                self.m_log.add(self.m_config.m_hostname, \
                    "Missing color parameter 202410112056");
                return False
            matching_light = Light.Light.CheckForMatch(head_id, color)
            if not matching_light:
                # No light matching this description in the config file
                #print("No light:", head_id)
                return False
            action = Action.Action()
            action.m_head_id = head_id
            action.m_light = matching_light
            action.m_color = color
            action.m_flashing = flashing
            self.m_action_list.append(action)
            if head_id not in self.m_head_list:
                self.m_head_list.append(head_id)
            return True

        if fixture == "number-plate":
            # number-plate is simply used for modifying the rule
            self.m_number_plate = number_plate
            return True

        self.m_log.add(self.m_config.m_hostname, p_aspect_cmd)
        self.m_log.add(self.m_config.m_hostname, "Invalid aspect 202410112057");
        return False


    # Check this Aspect against the Configuration of this signal.
    # Determine if this Aspect is approrpirate for this Config.
    # @returns True if this Aspect matches the Config, False otherwise
    #
    def check_config(self):
        if len(self.m_head_list) != self.m_config.head_count():
            #print("mismatch head count")
            return False

        # Only check for a number plate if it was specifically defined
        # in this Aspect.
        if self.m_number_plate is not None:
            if self.m_number_plate != self.m_config.m_number_plate_present:
                #print("mismatch number-plate")
                return False

        # This Aspect matches the Configuration
        return True


    # Execute the Actions assigned to this Aspect
    # @param p_source The source requesting the execution
    # @param p_log Log to print error messages
    # @returns True on success, False on failure
    #
    def execute(self, p_source, p_log):
        for action in self.m_action_list:
            if not action.execute(p_source, p_log):
                p_log.add("Aspect", "execute failed 202410160828")
                return False
        return True


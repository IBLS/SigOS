#
# Manage a command targeted to another SigOS device.
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

import Command
import Log


class TargetedCommand:

    # Create a new TargetedCommand
    # @param p_target The hostname of the target SigOS device where the
    #        command will be sent.
    # @param p_command The SigOS command that will be sent to p_target
    # @param p_hostname This signal's hostname
    # @param p_log References the logging object
    #
    def __init__(self, p_target, p_command, p_hostname, p_log):

        self.m_target = p_target
        self.m_command = p_command
        self.m_log = p_log

        # Does the target refer to me?
        self.m_local = False
        if p_hostname == self.m_target:
            self.m_local = True

    # Destructor
    #
    def __del__(self):
        pass


    # Execute this command
    # @returns True on success, False on error
    #
    def execute(self):
        if self.m_local:
            # Attempt to parse and execute the specified command line
            # print(line)
            (cmd_match, func_result, result_list) = Command.Command.ParseAndExec(self.m_command, self.m_target)
            if not cmd_match:
                msg = "Invalid command ["
                msg += self.m_command
                msg += "] target ["
                msg += self.m_target
                msg += "]"
                self.m_log.add(self.m_target, msg)
                return False

            if not func_result:
                msg = "Command failed ["
                msg += self.m_command
                msg += "] target ["
                msg += self.m_target
                msg += "]"
                self.m_log.add(self.m_target, msg)
                return False

            for out_line in result_list:
                self.m_log.add(self.m_target, out_line)

            return True

        # dnevil - temporary debug output
        msg = "Sending command ["
        msg += self.m_command
        msg += "] target ["
        msg += self.m_target
        msg += "]"
        print(msg)

        return True


    # @returns A string representation of this Detector
    #
    def __str__(self):
        s = "targeted_command:"
        s += str(self.m_target)
        s += ", command:"
        s += str(self.m_command)
        return s



#
# Class for modeling a single state in a state machine of SigOS
#
# Copyright (C) 2021-2025 Daris A Nevil - International Brotherhood of Live Steamers
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

import Log
import TargetedCommand

class State:

    # Create a single State in a State Machine
    # @param p_machine_name The name of this state machine this state belongs to
    # @param p_state_name The name of this state
    # @param p_command The command to be executed when entering this state
    # @param p_command_target The hostname of the target that will execute the command
    # @param p_trans_list The list of transitions out of this state.
    # @param p_hostname The name of this signal
    # @param p_log The Log file to print messages to.
    #
    def __init__(self, p_machine_name, p_state_name, p_command, p_command_target, p_trans_list, p_hostname, p_log):
        self.m_machine_name = p_machine_name
        self.m_state_name = p_state_name
        self.m_command = p_command
        self.m_command_target = p_command_target
        self.m_trans_list = p_trans_list
        self.m_log = p_log
        self.m_targeted_command = TargetedCommand.TargetedCommand(self.m_command_target, self.m_command, p_hostname, p_log)


    # Called by the StateMachine to see if this is the state to be entered.
    # @param p_state_name The name of the state to enter
    # @returns True if this state was entered, False otherwise
    #
    def enter(self, p_state_name):
        if p_state_name != self.m_state_name:
            return False

        # Initialize the State Transitions in this State
        for trans in self.m_trans_list:
            trans.enter()

        # Execute the command
        self.m_targeted_command.execute()

        return True


    # Test if the input will cause a transition to a new state.
    # @param p_input_name The name of the input to test
    # @returns The name of a new state on a matching input, or empty string
    #
    def test_input(self, p_input_name):
        for trans in self.m_trans_list:
            next_state = trans.test_input(p_input_name)
            if next_state:
                return next_state
        return ''


    # Test if this state has a timeout and it causes a transition to a new state.
    # @returns The name of a new state on a timeout, or empty string
    #
    def test_timeout(self):
        for trans in self.m_trans_list:
            next_state = trans.test_timeout()
            if next_state:
                return next_state
        return ''


    # @returns A string representation of this State object
    #
    def __str__(self):
        s  = "machine_name:"
        s += str(self.m_machine_name)
        s += ",state_name:"
        s += str(self.m_state_name)
        s += ","
        s += str(self.m_targeted_command)
        for trans in self.m_trans_list:
            s += ",{"
            s += str(trans)
            s += "}"
        return s


#
# Class representing and managing StateMachines
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

import Config
import Log
import Timestamp


class StateMachine:

    # Store each created StateMachine in this class list
    c_state_machine_list = list()


    # Create an object to encapsulate configuraton for state machines
    # @param p_machine_name The name of this StateMachine
    # @param p_initial_state The name of the initial state
    # @param p_state_list The list of States contained in this machine
    # @param p_log Reference to the Log object
    #
    def __init__(self, p_machine_name, p_initial_state, p_state_list, p_log)
        self.m_machine_name = p_machine_name
        self.m_initial_state = p_initial_state
        self.m_state_list = p_state_list
        self.m_log = p_log

        # Initialize current state
        self.m_current_state = None
        self.enter_state(self.m_initial_state)



    # Enter the given state
    # @param p_state_name The name of the State to enter
    # @returns True on success, False if invalid p_state_name
    #
    def enter_state(self, p_state_name):
        for state in self.m_state_list:
            if p_state_name == state.enter(p_state_name):
                self.m_current_state = state
                return True
        return False


    # Test a given input for a given StateMachine to see if it causes a transition.
    # @param p_state_machine_name The name of the StateMachine
    # @param p_input_name The name of the input parameter to test
    #
    @classmethod
    def TestInput(p_class, p_state_machine_name, p_input_name):
        for state_machine in p_class.c_state_machine_list:
            if p_state_machine_name == state_machine.m_machine_name:
                state_machine.test_input(p_input_name)


    # Test for transition cause by the given input name
    # @param p_input_name The input parameter to test
    #
    def test_input(self, p_input_name):
        next_state = self.m_current_state.test_input(p_input_name)
        if next_state:
            self.enter_state(next_state)


    # Perform periodic polling for all of the registered StateMachines.
    # Call this method only after loading all Config
    #
    @classmethod
    def Poll(p_class):
        for state_machine in p_class.c_state_machine_list:
            state_machine.poll()


    # Poll for state timeouts, transition if found
    #
    def poll(self):
        next_state = self.m_current_state.test_timeout()
        if next_state:
            self.enter_state(next_state)


    # @returns A string representation of this StateMachine
    #
    def __str__(self):
        s = "machine_name:"
        s += str(self.m_machine_name)
        s += ",initial_state:"
        s += str(self.m_initial_state)
        s += ",current_state:"
        s += str(self.m_current_state.m_state_name)
        for state in self.m_state_list:
            s += ",{"
            s += str(state)
            s += "}"
        return s


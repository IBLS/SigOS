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
    c_state_machine_file = None
    c_state_machine_list = list()
    # Perform poll every second
    c_poll_limit = 1.0
    c_poll_count = 0.0


    # Create an object to encapsulate configuraton for state machines
    # @param p_filename The file that created this state machine
    # @param p_machine_name The name of this StateMachine
    # @param p_initial_state The name of the initial state
    # @param p_state_list The list of States contained in this machine
    # @param p_log Reference to the Log object
    #
    def __init__(self, p_filename, p_machine_name, p_initial_state, p_state_list, p_log):
        StateMachine.c_state_machine_file = p_filename
        self.m_machine_name = p_machine_name
        self.m_initial_state = p_initial_state
        self.m_state_list = p_state_list
        self.m_log = p_log

        # Initialize current state
        self.m_current_state = None
        self.enter_state(self.m_initial_state)

        # Save the new instance in the class
        StateMachine.c_state_machine_list.append(self)


    # Enter the given state
    # @param p_state_name The name of the State to enter
    # @returns True on success, False if invalid p_state_name
    #
    def enter_state(self, p_state_name):
        for state in self.m_state_list:
            if state.enter(p_state_name):
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
    # @param p_poll_time The frequency this function is called, in
    #        fractions of seconds
    #
    @classmethod
    def Poll(p_class, p_poll_time):
        p_class.c_poll_count += p_poll_time
        if p_class.c_poll_limit < p_class.c_poll_count:
            p_class.c_poll_count = 0
            return

        for state_machine in p_class.c_state_machine_list:
            state_machine.poll()


    # Poll for state timeouts, transition if found
    #
    def poll(self):
        next_state = self.m_current_state.test_timeout()
        if next_state:
            self.enter_state(next_state)


    # Print all registered StateMachines
    #
    @classmethod
    def Print(p_class):
        for state_machine in p_class.c_state_machine_list:
            print(str(state_machine))


    # @returns A string representation of this StateMachine
    #
    def __str__(self):
        s  = "StateConfig file:"
        s += StateMachine.c_state_machine_file
        s += "\n machine_name:"
        s += str(self.m_machine_name)
        s += "\n  initial_state:"
        s += str(self.m_initial_state)
        s += "\n  current_state:"
        s += str(self.m_current_state.m_state_name)
        for state in self.m_state_list:
            s += "\n  {"
            s += str(state)
            s += "\n  }"
        return s


#
# Class representing and managing State Transitions
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
import Timestamp


class StateTrans:

    # Create a new State Transition object
    # @param p_machine_name The name of the StateMachine containing this transition
    # @param p_state_name The name of the State containing this transition
    # @param p_input_name The (optional) name of the input will move to the next state
    # @param p_timeout_sec The (optional) timeout that will move to the next state on expiration
    # @param p_next_state The name of the next state
    # @param p_log Reference to the Log object
    #
    def __init__(self, p_machine_name, p_state_name, p_input_name, p_timeout_sec, p_next_state, p_log):
        self.m_machine_name = p_machine_name
        self.m_state_name = p_state_name
        self.m_input_name = p_input_name
        self.m_timeout_sec = p_timeout_sec
        self.m_expire_time = None
        self.m_next_state = p_next_state
        self.m_log = p_log


    # Must be called when the StateMachine enters a State containing this transition.
    #
    def enter(self):
        if self.m_timeout_sec:
            self.m_expire_time = Timestamp.Timestamp;
            self.m_expire_time.expire_after(self.m_timeout_sec)
        else:
            self.m_expire_time = None


    # Test if the input will cause a transition to a new state.
    # @param p_input_name The name of the input to test
    # @returns The name of a new state on a matching input, or empty string
    #
    def test_input(self, p_input_name):
        if p_input_name == self.m_input_name:
            return self.m_next_state
        return ''


    # Test if this StateTrans has a timeout and it causes a transition to a new state.
    # @returns The name of a new state on a timeout, or empty string
    #
    def test_timeout(self):
        if self.m_expire_time and self.m_expire_time.expired():
            return self.m_next_state
        return ''


    # @returns A string representation of this StateTrans
    #
    def __str__(self):
        s  = "\n      next_state:"
        s += str(self.m_next_state)
        if self.m_input_name:
            s += "\n      input:"
            s += str(self.m_input_name)
        if self.m_timeout_sec:
            s += "\n      timeout-sec:"
            s += str(self.m_timeout_sec)
        if self.m_expire_time:
            s += "\n      expire_time:"
            s += str(self.m_expire_time)
        return s



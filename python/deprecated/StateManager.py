#
# StateManager, a class to mananage prioritized StateRequests
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

import StateRequest

class StateManager:


    # Initialize a new StateManager
    # @param p_manager_name The name of this StateManager.
    # @param p_state_names A list containing the state names that will be
    #       managed by this class.
    # Note: This class assumes that the number of states is equal to the
    #       number of elements in the list p_state_names (n).  It further
    #       assumes that the integer values of the states are in the
    #       range 0 to n-1.
    #       Finally, the priority of each state is assumed to be the
    #       integer value of its position in the list p_state_names,
    #       where the higher integer index values have the higher priority.
    #
    def __init__(self, p_manager_name, p_state_names):
        if (len(p_state_names) == 0):
            raise Exception('Invalid state names list in StateManager 202407251628')

        self.m_manager_name = p_manager_name
        self.m_state_names = p_state_names
        self.m_state_priority = 0
        self.m_default_state = 0
        self.m_active_states = None


    # Set the default state, which will become the current active state when there
    # are no active state requests.
    # @param p_state The integer default state.
    # 
    def set_default_state(self, p__state):
        if (p_state >= len(self.m_state_names)):
            raise Exception('Invalid default state in StateManager 202407251634')

        self.m_default_state = p_state


    # @returns The default state.
    #
    def get_default_state(self):
        return self.m_default_state


    # @returns The string name of the default state.
    #
    def get_default_name(self):
        return self.m_state_names[self.m_default_state]


    # @returns The string name of the given integer state.
    #
    def get_state_name(self, p_state):
        if (p_state >= len(self.m_state_names)):
            raise Exception('Invalid integer state 202407251650')
        return self.m_state_names[p_state]


    # Register a new StateRequest
    # @param p_request A StateRequest holding the who, what and when
    # @returns True if this is a new state, False if it already exists
    #
    def request_state(self, p_request):

        for i in range(len(self.m_active_states)):
            if (self.m_active_states[i].same_as(p_request)):
                # This state has already been registered
                return False

        # Add the new request
        self.m_active_states.append(p_reqeust)
        return True


    # Remove an active state request. Only removes a request by the specified sender.
    # @param p_state_request The active state to be released
    # @returns True if the state was found in the request list, False otherwise
    #
    def release_state(self, p_state_request):

        for i in range(len(self.m_active_states)):
            if (self.m_active_states[i].same_as(p_state_request)):
                # Remote the matching state from the list
                self.m_active_states.pop(i)
                return True

        # No matching state found
        return False


    # Remove all matching StateRequests, regardless of the requestor.
    # @param p_release The integer value of the state to remove
    # @returns True if p_state was found in the active states list, False otherwise
    #
    def release_state_all(self, p_state):
        for i in range(len(self.m_active_states)):
            if (self.m_active_states[i].get_state() == p_state):
                # Remove the state from the list
                self.m_active_states.pop(i)
                return True

        # No matching state found
        return False


    # Remove all StateRequests
    #
    def clear(self):
        m_active_states.clear()


    # Review all currently registerd StateRequests and determine which
    # state has the highest priority (e.g. this is the current active state).
    # \returns The current highest priority integer state. If no StateRequests are registered
    #          then the default state is returned.
    #
    def get_priority_state(self):
        if (not self.m_active_states):
            return self.m_default_state

        # Look for the highest integer state
        current_state = 0
        for i in range(len(self.m_active_states)):
            requested_state = m_active_states[i].get_state()
            if (requested_state > current_state):
                current_state = requested_state

        return current_state


    # @returns A human-readable representation of this StateManager.
    #
    def __str__(self):
        sm_str = self.m_manager_name
        sm_str += "\n"

        for i in range(len(self.m_active_states)):
            sm_str += self.m_active_states[i]
            sm_str += "\n"

        if (not self.m_active_states):
            sm_str += "No active requests\n"

        sm_str += "Current state: "
        priority_state = self.get_priority_state()
        sm_str += self.get_state_name(priority_state)


#
# Class representing State Requests
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

import Timestamp

class StateRequest:

    # Initialize a new StateRequest.
    # @param p_state_request The integer state being requested.
    # @param p_source The id of the requestor, usually IP addr.
    # @param p_timestamp The Timestamp of this request.
    #
    def __init__(self, p_state_request, p_source, p_timestamp):
        self.m_state_request = p_state_request
        self.m_source = p_source
        self.m_timestamp = p_timestamp


    # Compare this StateRequest to another. Don't use the timestamp in the comparison.
    # @param p_state_request The StateRequest being compare to
    # @returns True if the StateRequests match
    #
    def same_as(self, p_state_request):
        return ((self.m_state_request == p_state_request.m_state_request) and
                (self.m_source == p_state_request.m_source))


    # @returns The integer requested state
    # 
    def get_state(self):
        return self.m_state_request


    # @param p_state_names List of states names that correlate to the values
    #        assign to m_state_request
    # @returns A string representation of the StateRequest
    # 
    def __str__(self, p_state_names):
        # Print timestamp
        sr_str = self.m_timestamp
        sr_str += ': '

        # Print state name
        sr_str += p_state_names[self.m_state_request]
        sr_str += ', '

        // Print IP address of requestor
        sr_str += self.m_source

        return sr_str


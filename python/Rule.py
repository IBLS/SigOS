#
# Class for encapsulating a single operating rule for SigOS
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

import Aspect


class Rule:

    # Create a Rule object to encapsulates a single operating rule
    # @param p_rule The rule number assigned to this aspect. This is actaully a string,
    #               because some rules use alpha designators, e.g. "281" and "281A"
    # @param p_name The formal name classifcation, e.g. "Diverging-clear"
    # @param p_indication Descriptive instruction conveyed by the signal
    # @param p_priority The numeric (real or float) relative priority of this aspect
    # @param p_aspect An Aspect object that has already been evaluated.
    #
    def __init__(self, p_rule, p_name, p_indication, p_priority, p_aspect):
        self.m_rule = p_rule
        self.m_name = p_name
        self.m_indication = p_indication
        self.m_priority = p_priority
        self.m_aspect = p_aspect
        # Attributes to be set when the Rule is activated
        self.m_source = None


    # Make a shallow copy of this Rule
    #
    def copy(self):
        return type(self)(self.m_rule, self.m_name, self.m_indication, self.m_priority, self.m_aspect)


    # Execute all Aspect changes associated with this Rule
    # @param p_source The source requesting the execution
    # @param p_log Log to print error messages
    # @returns True on success, False on failure
    #
    def execute(self, p_source, p_log):
        if self.m_aspect:
            return self.m_aspect.execute(p_source, p_log)
        p_log.add("Rule", "Missing aspect 2020410151602")
        return False


    # @returns The relative priority of this Rule
    #
    def get_priority(self):
        return self.m_priority


    # @returns True if this Rule matches the given rule number
    # @param p_rule The number identifying this Rule
    #
    def match_by_rule(self, p_rule):
        return p_rule == self.m_rule


    # @returns True if this Rule matches the given rule number
    # @param p_name The name of this Rule
    #
    def match_by_name(self, p_name):
        return p_name == self.m_name


    # @returns A simple-to-read string representation of this rule
    #
    def simple_str(self):
        s = str(self.m_rule)
        s += ', '
        s += str(self.m_name)
        s += ', '
        s += str(self.m_indication)
        return s


    # @returns A string representation of this rule
    #
    def __str__(self):
        s = '"rule": "'
        s += str(self.m_rule)
        s += '", "name": "'
        s += str(self.m_name)
        s += '", "source": "'
        s += str(self.m_source)
        s += '", "indication": "'
        s += str(self.m_indication)
        s += '", "priority": "'
        s += str(self.m_priority)
        return s



#
# Class for encapsulating signal operating rules for SigOS
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

import io
import json
import Rule

class Rules:

    # Create an object to encapsulate all rules for a Signal
    # @param p_rule_file Filename of a json rules file
    #
    def __init__(self, p_rule_file):
        self.m_rule_file = p_rule_file
        fs = io.open(p_rule_file, mode='r')
        rd = json.load(fs)
        fs.close()

        self.m_rule_set = rd["rule-set"]
        self.m_source = rd["source"]
        self.m_author = rd["author"]
        self.m_default_rule = rd["default-rule"]

        rules = rd["rules"]

        self.m_rule_list = list()
        for rule in rules:
            robj = Rule.Rule(
                        rule["rule"],
                        rule["name"],
                        rule["indication"],
                        rule["priority"],
                        rule["condition"],
                        rule["aspect"])
            self.m_rule_list.append(robj)



    # Startup by activating the default Rule.
    # Call this once at system startup after the hardware has been initialized
    #
    def startup(self):
        self.activate_by_rule(self.m_default_rule)


    # Find and return the currently active Rule, or None
    #
    def find_active_rule(self):
        for rule in self.m_rule_list:
            if (rule.is_active()):
                return rule

        return None


    # Find and activiate the Rule by the given rule number
    # @param p_rule The rule number to activate
    # @returns True if the Rule was activated, False otherwise
    #
    def activate_by_rule(self, p_rule):
        active_priority = 0
        active_rule = self.find_active_rule()
        if (active_rule):
            active_priority = self.get_priority()

        for rule in self.m_rule_list:
            if (rule.match_by_rule(p_rule)):
                if (active_priority <= rule.get_priority()):
                    if (active_rule):
                        active_rule.deactivate()
                    rule.activate()
                    return True

        return False


    # Find and activiate the Rule by the given rule name
    # @param p_name The name of the Rule to activate
    # @returns True if the Rule was activated, False otherwise
    #
    def activate_by_name(self, p_name):
        active_priority = 0
        active_rule = self.find_active_rule()
        if (active_rule):
            active_priority = self.get_priority()

        for rule in self.m_rule_list:
            if (rule.match_by_name(p_name)):
                if (active_priority <= rule.get_priority()):
                    active_rule.deactivate()
                    rule.activate()
                    return True

        return False



    # Deactivate any active rule.
    #
    def deactivate(self):
        for rule in rules:
            rule.deactivate()


    # @returns A string representation of this rule set
    #
    def __str__(self):
        s = "rule-set: "
        s += self.m_rule_set
        s += "\nsource: "
        s += self.m_source
        s += "\nauthor: "
        s += self.m_author
        s += "\n"
        for rule in self.m_rule_list:
            s += str(rule)
            s += "\n"
        return s


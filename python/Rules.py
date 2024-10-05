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
import Log

class Rules:

    # Class variable for the Rules singleton object
    c_rules = None

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

        self.m_request_list = list()
        self.m_active_rule = None

        # Save this singleton
        Rules.c_rules = self



    # Startup by activating the default Rule.
    # Call this once at system startup after the hardware has been initialized
    # @param p_source The name of the source, should be this hostname
    #
    def startup(self, p_source):
        self.request_by_rule_or_name(self.m_default_rule, p_source)


    # Request activation of a rule by number or name
    # @param p_rule_or_name The rule number or name
    # @param p_source The name of the requestor
    # @returns True if valid request, False if invalid rule or name
    #
    def request_by_rule_or_name(self, p_rule_or_name, p_source):
        # Verify valid rule
        valid = False
        for rule in self.m_rule_list:
            if (rule.match_by_rule(p_rule_or_name):
                valid = True
                break
            if (rule.match_by_name(p_rule_or_name)):
                valid = True
                break
        if not valid:
            return false

        # Is the rule already in the list?
        for req in self.m_request_list:
            if ((req[0] == p_rule_or_name) and (req[1] == p_source)):
                # Request is already registered
                return True

        # Add as new request
        self.m_request_list.append([p_rule_or_name, p_source])
        return True


    #def activate_highest_rule(self):
    #    high_rule = self.m_request_list[0]
    #    for req in self.m_request_list:
    #        if (
            

    # Find and return the currently active Rule, or None
    #
    def find_active_rule(self):
        for rule in self.m_rule_list:
            if (rule.is_active()):
                return rule

        return None


    # Find and activiate the Rule by the given rule number or rule name
    # @param p_rule_or_name The rule number or name to activate
    # @param p_source The source requesting the action
    # @returns True on activation of new Rule, False if not found or not activated
    #
    def activate_by_rule_or_name(self, p_rule_or_name, p_source):
        active_priority = 0
        active_rule = self.find_active_rule()
        if (active_rule):
            active_priority = active_rule.get_priority()

        for rule in self.m_rule_list:
            if (rule.match_by_rule(p_rule_or_name) or rule.match_by_name(p_rule_or_name)):
                if (active_priority <= rule.get_priority()):
                    if (active_rule):
                        active_rule.deactivate()
                    rule.activate()
                    return True
                else:
                    break;

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


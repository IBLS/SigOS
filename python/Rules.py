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
                        rule["aspect"])
            self.m_rule_list.append(robj)

        # The request list is maintained in ascending order
        # according to rule priority.
        self.m_request_list = list()

        # Save a local Log object for convenience
        self.m_log = Log.Log()

        # Save this singleton
        Rules.c_rules = self



    # Startup by activating the default Rule.
    # Call this once at system startup after the hardware has been initialized
    # @param p_source The name of the source, should be this hostname
    #
    def startup(self, p_source):
        state = self.request_by_rule_or_name(self.m_default_rule, p_source)
        if state == 0:
            msg = "Invalid default rule: "
            msg += self.m_default_rule
            self.m_log.add(p_source, msg)
        if state == 1 or state == 2:
            msg = "Invalid pending default rule: "
            msg += self.m_default_rule
            self.m_log.add(p_source, msg)
        if state == 3:
            msg = "Activated default rule: "
            msg += self.m_default_rule
            self.m_log.add(p_source, msg)


    # Insert the given rule into the request list.
    # @p_rule The rule to be inserted
    # @p_source The name of the source making the request.
    # @returns True if the rule was inserted, false if the rule
    #          is already in the list.
    #
    def request(self, p_rule, p_source):
        index = len(self.m_request_list)
        for rule in reversed(self.m_request_list):
            if p_rule.m_rule == rule.m_rule:
                if p_rule.m_source == p_source:
                    # Already in the request list
                    return False
            if p_rule.m_priority > rule.m_priority:
                break
            index -= 1
        p_rule.m_source = p_source
        self.m_request_list.insert(index, p_rule)
        return True
        

    # Remove the specified rule from the request list.
    # @p_rule The rule to be removed
    # @p_source The name of the source making the request.
    # @returns True if the rule was removed, false if the rule
    #          was not in the list.
    #
    def release(self, p_rule, p_source):
        index = 0
        for rule in self.m_request_list:
            if p_rule.m_rule == rule.m_rule:
                if p_rule.m_source == rule.m_source:
                    self.m_request_list.pop(index)
                    return True
            index += 1
        return False
        

    # Remove the highest priority rule from the request list
    # @returns The removed rule, or None
    #
    def pop_active(self):
        if len(self.m_request_list) == 0:
            return None

        return self.m_request_list.pop()


    # @returns The highest priority rule in the list, or None if empty
    #
    def get_active_rule(self):
        if len(self.m_request_list) == 0:
            return None
        return self.m_request_list[-1]


    # Find and return a rule by number or name.
    # @p_rule_or_name A string of the rule number or name
    # @returns The matching rule, or None if not a valid rule.
    #
    def find_rule(self, p_rule_or_name):
        for rule in self.m_rule_list:
            if (rule.m_rule == p_rule_or_name):
                return rule
            if (rule.m_name == p_rule_or_name):
                return rule
        return None


    # Request activation of a rule by number or name
    # @param p_rule_or_name The rule number or name
    # @param p_source The name of the requestor
    # @returns state where:
    #          0 - if invalid rule or name
    #          1 - if the rule is already in the list
    #          2 - if the rule was added but not activated
    #          3 - if the rule was added and activated
    #
    def request_by_rule_or_name(self, p_rule_or_name, p_source):
        # Verify the request is a valid rule
        valid_rule = self.find_rule(p_rule_or_name)
        # Did we find a valid rule?
        if not valid_rule:
            return 0

        # Remember the current active rule
        pre_active_rule = self.get_active_rule()

        # Add the rule to the request list
        if not self.request(valid_rule, p_source):
            # This rule is already in the list
            return 1

        # Has the active rule changed?
        post_active_rule = self.get_active_rule()
        if pre_active_rule and pre_active_rule.m_rule == post_active_rule.m_rule:
            # No, same rule is in effect, no change required
            return 2

        # We have changed the current active rule
        if (pre_active_rule):
            s = "Released: "
            s += pre_active_rule.m_rule
            s += ":"
            s += pre_active_rule.m_name
            self.m_log.add(p_source, s)

        s = "Activated: "
        s += post_active_rule.m_rule
        s += ":"
        s += post_active_rule.m_name
        self.m_log.add(p_source, s)

        # TODO: Figure out how to change hardware state

        return 3


    # Release a rule by number or name
    # @param p_rule_or_name The rule number or name
    # @param p_source The name of the requestor
    # @returns state where:
    #          0 - if invalid rule or name
    #          1 - if the rule is was not in the request list
    #          2 - if the rule was released but was not activated
    #          3 - if the rule was activated and was released
    #
    def release_by_rule_or_name(self, p_rule_or_name, p_source):
        # Verify the release is a valid rule
        valid_rule = self.find_rule(p_rule_or_name)
        # Did we find a valid rule?
        if not valid_rule:
            return 0

        if len(self.m_request_list) < 2:
            return 0

        # Don't remove the default rule
        if (p_rule_or_name == self.m_default_rule) or \
           (p_rule_or_name == self.m_default_rule):
            return 0

        # Remember the current active rule
        pre_active_rule = self.get_active_rule()

        # Release the rule from the request list
        if not self.release(valid_rule, p_source):
            # This rule was not in the request list
            return 1

        # Has the active rule changed?
        post_active_rule = self.get_active_rule()
        if (pre_active_rule.m_rule == post_active_rule.m_rule):
            # No, same rule is in effect, no change required
            return 2

        # We have changed the current active rule
        if (pre_active_rule):
            s = "Released: "
            s += pre_active_rule.m_rule
            s += ":"
            s += pre_active_rule.m_name
            self.m_log.add(p_source, s)

        s = "Activated: "
        s += post_active_rule.m_rule
        s += ":"
        s += post_active_rule.m_name
        self.m_log.add(p_source, s)

        # TODO: Figure out how to change hardware state

        return 3


    # @returns A string representation of the request list
    #
    def request_list(self):
        out = list()
        for rule in self.m_request_list:
            s = str(rule)
            out.append(s)
        return out


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


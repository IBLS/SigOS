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

        self.m_rule_set = rd["rule_set"]
        self.m_source = rd["source"]
        self.m_author = rd["author"]
        rules = rd["rules"]

        self.m_rule_array = []
        for rule in rules:
            robj = Rule.Rule(
                        rule["rule"],
                        rule["name"],
                        rule["indication"],
                        rule["priority"],
                        rule["condition"],
                        rule["aspect"])
            self.m_rule_array.append(robj)


    # @returns A string representation of this rule set
    #
    def __str__(self):
        s = "rule_set: "
        s += self.m_rule_set
        s += "\nsource: "
        s += self.m_source
        s += "\nauthor: "
        s += self.m_author
        s += "\n"
        for rule in self.m_rule_array:
            s += str(rule)
            s += "\n"
        return s


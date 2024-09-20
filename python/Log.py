#
# Class for recording events into a Log for SigOS
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

class Log:

    # Class variables

    # The log is stored in these parallel lists, limited in size
    # by c_log_limit
    c_log_time = list()
    c_log_source = list()
    c_log_text = list()

    # Limits the number of lines maintained in c_log_xxx
    c_log_limit = 32


    def __init__(self):
        pass


    def add(self, p_source, p_text):
        # Add the log entry
        ts = Timestamp.Timestamp()
        Log.c_log_time.append(str(ts))
        Log.c_log_source.append(p_source)
        Log.c_log_text.append(p_text)

        # Remove oldest entry if necessary
        if (len(Log.c_log_time) > Log.c_log_limit):
            Log.c_log_time.pop(0)
            Log.c_log_source.pop(0)
            Log.c_log_text.pop(0)

    # @returns A string representation of this rule set
    #
    def __str__(self):
        s = ""
        for i in range(len(Log.c_log_time)):
            s += str(Log.c_log_time[i])
            s += " "
            s += Log.c_log_source[i]
            s += " "
            s += Log.c_log_text[i]
            s += "\n"
        return s


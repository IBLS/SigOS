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


    # Add new entry to the log
    # @param p_source Name of the source associated with the log entry
    # @param p_text Test string to add to the log
    #
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


    # Get an entry from the log
    # @param p_index Zero gets the most recent entry, 1 gets the next
    #                most recent entry, etc
    # @returns A string of the specified log entry
    #
    def get_single(self, p_index):
        if (p_index >= len(Log.c_log_time)):
            return None
        s = str(Log.c_log_time[p_index])
        s += " "
        s += Log.c_log_source[p_index]
        s += " "
        s += Log.c_log_text[p_index]
        return s


    # Get all entries in the log
    # @return A list of log entries, oldest to newest
    #
    def get_all(self):
        l = list()
        for i in range(len(Log.c_log_time)):
            s = self.get_single(i)
            l.append(s)
        return s


    # Get all entries in the log
    # @return A list of log entries, newest to oldest
    #
    def get_all_rev(self):
        l = list()
        for i in range(len(Log.c_log_time)-1, -1):
            s = self.get_single(i)
            l.append(s)
        return s


    # @returns The number of entries in the log
    #
    def get_num_entries(self):
        return len(Log.c_log_time)


    def unit_test(self):
        log1 = Log()
        log1.add("Me", "Message 1")
        log1.add("You", "Message 2")
        if (log1.get_num_entries() != 2):
            print("Failed 1000\n")

        log2 = Log()
        for i in range(Log.c_log_limit):
            text = "Message " + str(i)
            log2.add("ABC", text)

        if (log2.get_num_entries() != Log.c_log_limit):
            print("Failed 1010\n")

        log2.add("EFG", "Message X")
        if (log2.get_num_entries() != Log.c_log_limit):
            print("Failed 1020\n")

        print("Unit tests completed\n") 

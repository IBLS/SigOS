#
# General Timestamp class
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

import time

class Timestamp:

    # Initialize the new Timestamp to the current time
    #
    def __init__(self):
        self.m_time = time.time()
        self.m_expire_sec = 0


    # Set the future expire time for this timestamp.
    # @param p_seconds The number of seconds from the creation of this object
    #        before it expires.
    #
    def expire_after(self, p_seconds):
        self.m_expire_sec = p_seconds;


    # @returns True if this Timestamp has expired
    #
    def expired(self):
        if (self.m_time + self.m_expire_sec) > time.time():
            return True

        return False


    # @returns The time when the Timestamp will expire (or did expire)
    #
    def  get_expire_time(self):
        return self.m_time + self.m_expire_sec;


    # @returns The time when the Timestamp was created and initialized
    #
    def get_timestamp(self):
        return self.m_time


    # @returns A human-readable string value of this Timestamp
    #
    def __str__(self):
        ltime = time.localtime(self.m_time)
        s = "{:04n}".format(ltime[0])
        s += "/"
        s += "{:02n}".format(ltime[1])
        s += "/"
        s += "{:02n}".format(ltime[2])
        s += " "
        s += "{:02n}".format(ltime[3])
        s += ":"
        s += "{:02n}".format(ltime[4])
        s += ":"
        s += "{:02n}".format(ltime[5])
        return s


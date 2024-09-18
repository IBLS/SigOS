#
# Class for modeling a Semaphore in SigOS
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

class Semaphore:

    # Create a Semaphore object
    # @param p_head_id The identifier (number) of the Head containing this semaphore,
    #                  1 is the highest head, 2 is the next highest, etc
    # @param p_semaphore_id The identifier (number) of the Semaphore, 1 is highest on mast,
    #             2 is next highest, etc
    # @param p_degrees_per_second Speed in which the Semaphore flag moves
    #
    def __init__(self, p_head_id, p_semaphore_id, p_degrees_per_second):
        self.m_head_id = p_head_id
        self.m_semaphore_id = p_semaphore_id
        self.m_degrees_per_second = p_degrees_per_second


    # @returns A string representation of this Semaphore
    #
    def __str__(self):
        s = "  semaphore: "
        s += str(self.m_semaphore_id)
        s += "\n    head-id: "
        s += str(self.m_head_id)
        s += "\n    degrees-per-second: "
        s += str(self.m_degrees_per_second)
        return s


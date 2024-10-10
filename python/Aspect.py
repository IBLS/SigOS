#
# Class for managing the Aspect of a Rule
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

import Action

class Aspect:

    def __init__(self, p_aspect_commands):
        self.m_aspect_commands = p_aspect_commands
        self.m_action_list = list()


    # Evaluate the aspect string. Save the condition results,
    # but do not execute the actions.
    # @returns True on success, False on evaluation error
    #
    def eval(self):
        cmds = self.m_aspect_commands.split(';')
        for cmd in cmds:
            words = cmd.split()
            fixture = words[0]

            # Get the common 'head' argument
            head_arg = words[1].split(':')
            if head_arg[0] != 'head':
                return False
            head = int(head_arg[1])

            if fixture == "semaphore":
                angle_arg = words[2].split(':')
                if angle_arg[0] != 'angle':
                    return False
                angle = int(angle_arg[1])
                action = Action.Action()
                action.m_head = head
                action.m_semaphore = True
                action.m_angle = angle
                self.m_action_list.append(action)
                continue

            if fixture == "lumen":
                color_arg = words[2].split(':')
                if color_arg[0] != 'color':
                    return False
                color = color_arg[1]
                flashing = False
                if len(words) >= 4:
                    flashing = words[3]
                action = Action.Action()
                action.m_head = head
                action.m_lumen = True
                action.m_color = color
                action.m_flashing = flashing
                self.m_action_list.append(action)


#
# Defines a Command for SigOS
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

class Command:

    # Define a command
    # @param p_word_list The list of words for the command
    # @param p_desc Text that describes the command, output of help()
    # @param p_func A function that will execute the command
    #@param p_command_list A list that this command will be appended to
    #
    def __init__(self, p_word_list, p_desc, p_func, p_command_list):
        self.m_word_list = p_word_list
        self.m_desc = p_desc
        self.m_func = p_func
        self.m_command_list = p_command_list
        p_command_list.append(self)
        if (!self.m_func):
            raise Exception('Undefined Command function 02407231742')


    # Compare the input to the command, and if a match, execute the associated function.
    # @param p_words An array of input words.
    # @param p_words_len The number of strings in p_words.
    # @param p_func_result The result of the function, if called
    # @param p_output Reference to a string to receive user-text from the command.
    # @returns (cmd_match, func_result, func_str), where
    #          cmd_match is true if this command matches
    #          func_result is the result of the function
    #          func_str is the string result from the function
    #
    def parse_and_exec(self, p_input_words)

        # Test if the input words invoke this command
        if (len(p_input_words) != len(self.m_word_list)):
            return False, False, ""

        words = []
        macros = []
        for i in range(len(p_input_words)):
            # Test for a macro to be parsed
            if (p_input_words[i] == '$'):
                # Let the m_func expand the macro, if called
                macros.append(p_input_words[i]);
                continue;

            if (p_input_words[i] != self._word_list[i])
                return False, False, ''

            # Save the list of non-macro constant words
            words.append(p_input_words[i])

        # Execute the function and provide the output value
        return self.m_func(words, macros)


    # Build text that describes this command
    # @returns The help string
    #
    def help(self):
        first = True
        help = ''

        # Include the command words
        for i in range(len(p_input_words)):
            if (first):
                first = False
            else:
                help += ' '

            help += self.m_word_list[i]

        # Then add the description
        help += ' : ';
        help += self.m_desc

        # Caller must add his own newline if needed
        return help


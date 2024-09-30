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

class Command:

    # Class variable containing the list of all registered commands.
    c_command_list = list()

    # Define a command
    # @param p_word_list The list of words for the command
    # @param p_desc Text that describes the command, output of help()
    # @param p_func A function that will execute the command
    #
    def __init__(self, p_word_list, p_desc, p_func):
        self.m_word_list = p_word_list
        self.m_desc = p_desc
        self.m_func = p_func
        Command.c_command_list.append(self)
        if (not self.m_func):
            raise Exception('Undefined Command function 02407231742')


    # Create a list of help strings describing the registered commands
    # @returns A list of strings
    #
    @staticmethod
    def Help():
        help_list = list()
        for cmd in Command.c_command_list:
            s = ""
            for word in cmd.m_word_list:
                if (word[0] == "$"):
                    s += word[1:]
                    s += " "
                else:
                    s += word
                    s += " "
            s += ": "
            s += cmd.m_desc
            help_list.append(s)
        return help_list


    # Attempt to execute the command given by the list of words
    # @param p_input_words A list of command words and parameters
    # @returns (cmd_match, func_result, result_list), where
    #          cmd_match is true if this command matches
    #          func_result is the result of the function
    #          result_list is a list of strings from the function
    #
    @staticmethod
    def ParseAndExec(p_input_words):
        for cmd in Command.c_command_list:
            (cmd_match, func_result, result_list) = cmd.parse_and_exec(p_input_words)
            if (cmd_match):
                return True, func_result, result_list
        inv_cmd = ["Invalid command"]
        return False, False, inv_cmd


    # Compare the input to the command, and if a match, execute the associated function.
    # @param p_words An array of input words.
    # @param p_words_len The number of strings in p_words.
    # @param p_func_result The result of the function, if called
    # @param p_output Reference to a string to receive user-text from the command.
    # @returns (cmd_match, func_result, result_list), where
    #          cmd_match is true if this command matches
    #          func_result is the result of the function
    #          result_list is a list of strings from the function
    #
    def parse_and_exec(self, p_input_words):

        # Test if the input words invoke this command
        if (len(p_input_words) != len(self.m_word_list)):
            empty = list()
            return False, False, empty

        for i in range(len(p_input_words)):
            # '$' represents a variable, skip it
            if (self.m_word_list[i][0] == '$'):
                continue

            if (p_input_words[i] != self.m_word_list[i]):
                return False, False, ''

        # Execute the function and provide the output value
        (func_result, result_list) = self.m_func(p_input_words)
        return True, func_result, result_list



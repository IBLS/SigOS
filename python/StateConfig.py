#
# Class for parsing the StateMachine json config files.
#
# Copyright (C) 2021-2025 Daris A Nevil - International Brotherhood of Live Steamers
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
import StateMachine
import State
import StateTrans


class StateConfig:

    # Create an object to encapsulate configuraton for state machines
    # @param p_file Filename of a json state file
    # @param p_hostname The hostname of this signal
    # @param p_log Reference to the Log object
    #
    def __init__(self, p_file, p_hostname, p_log):

        # Read the json file and parse
        fs = io.open(p_file, 'r')
        json_state = json.load(fs)
        fs.close()

        state_machines_json = json_state["state-machines"]
        for state_machine_json in state_machines_json:
            machine_name = state_machine_json["machine-name"]
            initial_state = state_machine_json["initial-state"]

            state_list = list()
            states_json = state_machine_json["states"]
            for state_json in states_json:
                state_name = state_json["name"]
                command = state_json["command"]
                command_target = state_json["command-target"]

                transition_list = list()
                for transition_json in state_json["transition"]:
                    # next-state is a required attribute
                    next_state = transition_json["next-state"]

                    input_name = None
                    if "input" in transition_json:
                        input_name = transition_json["input"]

                    timeout_sec = 0
                    if "timeout-sec" in transition_json:
                        timeout_sec = transition_json["timeout-sec"]

                    # Create a new State Transition object
                    state_trans = StateTrans.StateTrans(machine_name, state_name, input_name, timeout_sec, next_state, p_log)
                    transition_list.append(state_trans)

                # Create a new State object
                state = State.State(machine_name, state_name, command, command_target, transition_list, p_hostname, p_log)
                state_list.append(state)

            # Create a new StateMachine object
            # The StateMachine class holds a list of all StateMachine objects
            StateMachine.StateMachine(p_file, machine_name, initial_state, state_list, p_log)



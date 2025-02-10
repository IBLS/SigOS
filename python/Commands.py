#
# Commands for SigOS
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

import os
import Command
import Log
import Config
import Rules
import TelnetServer

SigOS_Version = "20241022"

def fn_help(p_word_list, p_source):
    return True, Command.Command.Help()

wl = ["help"]
Command.Command(wl, "Provide a list of supported commands", fn_help)


def fn_request(p_word_list, p_source):
    rule_or_name = p_word_list[1]
    rules = Rules.Rules.c_rules
    if rule_or_name == "list":
        out = rules.request_list()
        return True, out
    out = list()
    state = rules.request_by_rule_or_name(rule_or_name, p_source)
    if state == 0:
        msg = "Invalid: "
        msg += rule_or_name
        out.append(msg)
    if state == 1:
        msg = "Pending: "
        msg += rule_or_name
        out.append(msg)
    if state == 2:
        msg = "Active: "
        msg += rule_or_name
        out.append(msg)
    if state == 3:
        msg = "Activated: "
        msg += rule_or_name
        out.append(msg)
    return True, out

wl = ["request", "${rule}|{name}|list"]
Command.Command(wl, "Request activation of a Rule by number or name", fn_request)


def fn_release(p_word_list, p_source):
    rule_or_name = p_word_list[1]
    out = list()
    rules = Rules.Rules.c_rules
    state = rules.release_by_rule_or_name(rule_or_name, p_source)
    if state == 0:
        msg = "Invalid: "
        msg += rule_or_name
        out.append(msg)
    if state == 1:
        msg = "Not requested: "
        msg += rule_or_name
        out.append(msg)
    if state == 2:
        msg = "Released: "
        msg += rule_or_name
        out.append(msg)
    if state == 3:
        msg = "Deactivated: "
        msg += rule_or_name
        out.append(msg)
        active_rule = rules.get_active_rule()
        msg = "Activated: "
        msg += active_rule.m_rule
        out.append(msg)
    return True, out

wl = ["release", "${rule}|{name}"]
Command.Command(wl, "Release previous Rule activation by number or name", fn_release)


def fn_active(p_word_list, p_source):
    out = list()
    rules = Rules.Rules.c_rules
    active_rule = rules.get_active_rule()
    msg = str(active_rule)
    out.append(msg)
    return True, out

wl = ["active"]
Command.Command(wl, "Show the active Rule", fn_active)


def fn_rules(p_word_list, p_source):
    rules = Rules.Rules.c_rules
    out = rules.supported_rules()
    return True, out

wl = ["rules"]
Command.Command(wl, "Print the list of supported Rules", fn_rules)


def fn_number_plate(p_word_list, p_source):
    config = Config.Config.c_config
    out = ["None"]
    if config.m_number_plate and (len(config.m_number_plate) > 0):
        out = [config.m_number_plate]
    return True, out

wl = ["number-plate"]
Command.Command(wl, "Show the number-plate, or None", fn_number_plate)


def fn_log(p_word_list, p_source):
    global g_log
    log = Log.Log()
    all_logs = log.get_all()
    return True, all_logs

wl = ["log"]
Command.Command(wl, "Print the full Log", fn_log)


def fn_log_n(p_word_list, p_source):
    try:
        index = int(p_word_list[1])
    except:
        err = ["Invalid index"]
        return False, err
    log = Log.Log()
    one_log = log.get_single(index)
    return True, one_log

wl = ["log", "${entry_num}"]
Command.Command(wl, "Print a specified line of the log Log", fn_log_n)


def fn_close(p_word_list, p_source):
    log = Log.Log()
    log.add(p_source, "Disconnected client session")
    msg = list()
    if not TelnetServer.TelnetServer.Close(p_source):
        msg.append("Failed to close connection")
    else:
        msg.append("ok")
    return True, msg

wl = ["close"]
Command.Command(wl, "Close the current client connection", fn_close)


def fn_os(p_word_list, p_source):
    out = list()
    out.append("SigOS " + SigOS_Version)
    out.extend(os.uname())
    return True, out

wl = ["os"]
Command.Command(wl, "Show operating system and hardware info", fn_os)



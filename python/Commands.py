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

import Command
import Log


def fn_help(p_word_list, p_client):
    return True, Command.Command.Help()

wl = ["help"]
Command.Command(wl, "Provide a list of supported commands", fn_help)


def fn_request(p_word_list, p_client):
    ok = ["ok"]
    return True, ok

wl = ["request", "${rule}|{name}"]
Command.Command(wl, "Request activation of a Rule by number or name", fn_request)


def fn_release(p_word_list, p_client):
    ok = ["ok"]
    return True, ok

wl = ["release", "${rule}|{name}"]
Command.Command(wl, "Release previous Rule activation by number or name", fn_release)


def fn_log(p_word_list, p_client):
    log = Log.Log()
    all_logs = log.get_all()
    return True, all_logs

wl = ["log"]
Command.Command(wl, "Print the full Log", fn_log)


def fn_log_n(p_word_list, p_client):
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


def fn_close(p_word_list, p_client):
    source = str(p_client.m_client_addr)
    log = Log.Log()
    log.add(source, "Disconnected client session")
    p_client.close()
    ok = ["ok"]
    return True, ok

wl = ["close"]
Command.Command(wl, "Close the current client connection", fn_close)



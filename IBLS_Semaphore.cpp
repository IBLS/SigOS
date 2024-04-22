/*
 * Control code for Semaphore Signals
 *
 * Copyright (C) 2021 Daris A Nevil - International Brotherhood of Live Steamers
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * DARIS A NEVIL, OR ANY OTHER CONTRIBUTORS BE LIABLE FOR ANY CLAIM,
 * DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
 * OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
 * OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 * 
 */

#include "IBLS_Semaphore.h"


// ESP01 Pinout
// Pin 1 - GND
// Pin 2 - GPIO1/UOTXD
// Pin 3 - GPIO2
// Pin 4 - Ch_PD/Ch_EN High=On, Low=Off/low current
// Pin 5 - GPIO0/SPI_CS2 GND at power-on to program
// Pin 6 - /Reset
// Pin 7 - GPIO3/UORXD
// Pin 8 - VCC
//
// Semaphore Usage
//
void power_up_pinmode(void)
{
    // Pin 2 - GPIO1 - LED drive for Sempahore Light
    pinMode(2, OUTPUT);

    // Pin 5 - GPIO0 - Servo out with external pullup
    pinMode(5, OUTPUT);

    // Pin 3 - GPIO2 - Factory Defaults on Power-up when low - external pullup
    pinMode(3, INPUT);
}


// Keep a list of all the commands defined
CommandList_t CommandList;

bool ProcessCommand(EndpointClient p_client, String& p_command)
{
    Timestamp cmd_ts;
    IPAddress source_ip = p_client.remoteIP();

    // Break p_command into words
    // Convert String to character array to simplify processing
    static char cmd_buf[1024];
    size_t cmd_buf_len = sizeof(cmd_buf) - 1; // Allow for null terminator
    p_command.toCharArray(cmd_buf, cmd_buf_len);
    if (cmd_buf_len > p_command.length())
    {
        cmd_buf_len = p_command.length();
    }

    Array<const char*> cmd_word_arr;
    const char* next_word = cmd_buf;
    for (size_t i = 0; i < cmd_buf_len; ++i)
    {
        if (isSpace(cmd_buf[i]))
        {
            cmd_word_arr[i] = 0;
            next_word++;
            continue;
        }

        // Save the word
        cmd_word_arr.push_back(next_word);

        // Find the end of the word
        while (i < cmd_buf_len)
        {
            if (isSpace(cmd_buf[i]))
            {
                break;
            }

            ++i;
        }
    }

    // Null terminate the last word
    cmd_word_arr[cmd_buf_len] = 0;

    const char** cmd_words = cmd_word_arr.data();
    bool cmd_found = false;
    for (size_t i = 0; i < CommandList.size(); ++i)
    {
        bool cmd_result = false;
        String cmd_output;
        cmd_found = CommandList[i]->parse_and_exec(
            cmd_words, cmd_word_arr.size(), cmd_result, cmd_output, cmd_ts, source_ip);

        if (!cmd_found)
        {
            continue;
        }

        p_client.print("\n");
        p_client.print(cmd_output);
        p_client.print("\n>");
        p_client.flush();
        break;
    }

    if (!cmd_found)
    {
        p_client.print("Error: command not found\n");
        p_client.print("\n>");
        p_client.flush();
    }

    return cmd_found;
}

// Print the help string
void Help(String& p_help)
{
    for (size_t i = 0; i < CommandList.size(); ++i)
    {
        CommandList[i]->help(p_help);
    }
}


bool f_help(Command* p_command, String& p_output)
{
    Help(p_output);
    return true;
}
const char* cmd0[] = {"help"};
Command cmd_help(
    cmd0,
    ELEMENTS_OF(cmd0),
    "Print this help text",
    *f_help,
    CommandList);


// The Lumen_State variable determines the state of the Semaphore Light
static const char* Lumen_State_Names[] =
{
    "off",
    "on",
    "blink-slow",
    "blink-fast"
};
#define Lumen_State_Off         0
#define Lumen_State_On          1
#define Lumen_State_Blink_Slow  2
#define Lumen_State_Blink_Fast  3

StateMgr Lumen_State(Lumen_State_Names, ELEMENTS_OF(Lumen_State_Names));


// Command: state request lumen off
bool f_state_lumen_request_off(Command* p_command, String& p_output)
{
    IPAddress source_ip = p_command->get_source_ip();
    Timestamp timestamp = p_command->get_timestamp();
    StateRequest request(Lumen_State_Off, source_ip, timestamp);
    return Lumen_State.request_state(request);
}
const char* cmd100[] = {"state", "lumen", "request", "off"};
Command cmd_state_lumen_request_off(
    cmd100,
    ELEMENTS_OF(cmd100),
    "Request semphore enter illumination off state",
    *f_state_lumen_request_off,
    CommandList);


// Command: state release lumen off
bool f_state_lumen_release_off(Command* p_command, String& p_output)
{
    IPAddress source_ip = p_command->get_source_ip();
    Timestamp timestamp = p_command->get_timestamp();
    StateRequest release(Lumen_State_Off, source_ip, timestamp);
    return Lumen_State.release_state(release);
}
const char* cmd110[] = {"state", "lumen", "release", "off"};
Command cmd_state_lumen_release_off(
    cmd110,
    ELEMENTS_OF(cmd110),
    "Relinquish illumination off state request",
    *f_state_lumen_release_off,
    CommandList);


bool f_state_lumen_request_on(Command* p_command, String& p_output)
{
    IPAddress source_ip = p_command->get_source_ip();
    Timestamp timestamp = p_command->get_timestamp();
    StateRequest request(Lumen_State_On, source_ip, timestamp);
    return Lumen_State.request_state(request);
}
const char* cmd200[] = {"state", "lumen", "request", "on"};
Command cmd_state_lumen_request_on(
    cmd200,
    ELEMENTS_OF(cmd200),
    "Request sempahore enter illumination on state",
    *f_state_lumen_request_on,
    CommandList);


bool f_state_lumen_release_on(Command* p_command, String& p_output)
{
    IPAddress source_ip = p_command->get_source_ip();
    Timestamp timestamp = p_command->get_timestamp();
    StateRequest release(Lumen_State_On, source_ip, timestamp);
    return Lumen_State.release_state(release);
}
const char* cmd300[] = {"state", "lumen", "release", "on"};
Command cmd_state_lumen_release_on(
    cmd300,
    ELEMENTS_OF(cmd300),
    "Relinquish illumination on state",
    *f_state_lumen_release_on,
    CommandList);


bool f_state_lumen_request_blink_slow(Command* p_command, String& p_output)
{
    IPAddress source_ip = p_command->get_source_ip();
    Timestamp timestamp = p_command->get_timestamp();
    StateRequest request(Lumen_State_Blink_Slow, source_ip, timestamp);
    return Lumen_State.request_state(request);
}
const char* cmd400[] = {"state", "lumen", "request", "blink-slow"};
Command cmd_state_lumen_request_blink_slow(
    cmd400,
    ELEMENTS_OF(cmd400),
    "Request sempahore enter illumination blink slow state",
    *f_state_lumen_request_blink_slow,
    CommandList);


bool f_state_lumen_release_blink_slow(Command* p_command, String& p_output)
{
    IPAddress source_ip = p_command->get_source_ip();
    Timestamp timestamp = p_command->get_timestamp();
    StateRequest release(Lumen_State_Blink_Slow, source_ip, timestamp);
    return Lumen_State.release_state(release);
}
const char* cmd500[] = {"state", "lumen", "release", "blink-slow"};
Command cmd_state_lumen_release_blink_slow(
    cmd500,
    ELEMENTS_OF(cmd500),
    "Relinquish illumination blink slow state",
    *f_state_lumen_release_blink_slow,
    CommandList);


bool f_state_lumen_request_blink_fast(Command* p_command, String& p_output)
{
    IPAddress source_ip = p_command->get_source_ip();
    Timestamp timestamp = p_command->get_timestamp();
    StateRequest request(Lumen_State_Blink_Fast, source_ip, timestamp);
    return Lumen_State.request_state(request);
}
const char* cmd600[] = {"state", "lumen", "request", "blink-fast"};
Command cmd_state_lumen_request_blink_fast(
    cmd600,
    ELEMENTS_OF(cmd600),
    "Request sempahore enter illumination blink fast state",
    *f_state_lumen_request_blink_fast,
    CommandList);


bool f_state_lumen_release_blink_fast(Command* p_command, String& p_output)
{
    IPAddress source_ip = p_command->get_source_ip();
    Timestamp timestamp = p_command->get_timestamp();
    StateRequest release(Lumen_State_Blink_Fast, source_ip, timestamp);
    return Lumen_State.release_state(release);
}
const char* cmd700[] = {"state", "lumen", "release", "blink-fast"};
Command cmd_state_lumen_release_blink_fast(
    cmd700,
    ELEMENTS_OF(cmd700),
    "Relinquish illumination blink fast state",
    *f_state_lumen_release_blink_fast,
    CommandList);



bool f_state_lumen_release_all(Command* p_command, String& p_output)
{
    Lumen_State.reset_state();
    return true;
}
const char* cmd750[] = {"state", "lumen", "release", "all"};
Command cmd_state_lumen_release_all(
    cmd750,
    ELEMENTS_OF(cmd750),
    "Relinquish all illumination requested states, returning to default state",
    *f_state_lumen_release_all,
    CommandList);



bool f_state_lumen_print(Command* p_command, String& p_output)
{
    return Lumen_State.print(p_output);
}
const char* cmd800[] = {"state", "lumen", "print"};
Command cmd_state_lumen_print(
    cmd800,
    ELEMENTS_OF(cmd800),
    "Print illumination state",
    *f_state_lumen_print,
    CommandList);



bool f_state_lumen_default_off(Command* p_command, String& p_output)
{
    Lumen_State.set_default_state(Lumen_State_Off);
    return true;
}
const char* cmd1010[] = {"state", "lumen", "default", "off"};
Command cmd_state_lumen_default_off(
    cmd1010,
    ELEMENTS_OF(cmd1010),
    "Set default illumination state to off",
    *f_state_lumen_default_off,
    CommandList);



bool f_state_lumen_default_on(Command* p_command, String& p_output)
{
    Lumen_State.set_default_state(Lumen_State_On);
    return true;
}
const char* cmd1020[] = {"state", "lumen", "default", "on"};
Command cmd_state_lumen_default_on(
    cmd1020,
    ELEMENTS_OF(cmd1020),
    "Set default illumination state to on",
    *f_state_lumen_default_on,
    CommandList);



bool f_state_lumen_default_blink_slow(Command* p_command, String& p_output)
{
    Lumen_State.set_default_state(Lumen_State_Blink_Slow);
    return true;
}
const char* cmd1030[] = {"state", "lumen", "default", "blink-slow"};
Command cmd_state_lumen_default_blink_slow(
    cmd1030,
    ELEMENTS_OF(cmd1030),
    "Set default illumination state to blink-slow",
    *f_state_lumen_default_blink_slow,
    CommandList);



bool f_state_lumen_default_blink_fast(Command* p_command, String& p_output)
{
    Lumen_State.set_default_state(Lumen_State_Blink_Fast);
    return true;
}
const char* cmd1040[] = {"state", "lumen", "default", "blink-fast"};
Command cmd_state_lumen_default_blink_fast(
    cmd1040,
    ELEMENTS_OF(cmd1040),
    "Set default illumination state to blink-fast",
    *f_state_lumen_default_blink_fast,
    CommandList);



bool f_state_lumen_default_print(Command* p_command, String& p_output)
{
    p_output += Lumen_State.get_default_name();
    return true;
}
const char* cmd1050[] = {"state", "lumen", "default", "print"};
Command cmd_state_lumen_default_print(
    cmd1050,
    ELEMENTS_OF(cmd1050),
    "Print the default illumination state",
    *f_state_lumen_default_print,
    CommandList);



bool f_state_lumen_set_priority(Command* p_command, String& p_output)
{
    for (int pri = 0; pri < ELEMENTS_OF(Lumen_State_Names); ++pri)
    {
        const char* macro = p_command->get_macro(pri);
        if (!macro)
        {
            p_output = "Error: Missing parameters";
            return false;
        }

        bool found = false;
        for (int state = 0; state < ELEMENTS_OF(Lumen_State_Names); ++state)
        {
            if (strcmp(macro, Lumen_State_Names[state]) == 0)
            {
                Lumen_State.set_priority(state, pri);
                found = true;
                break;
            }
        }

        if (!found)
        {
            p_output = "Error: Invalid state name";
            return false;
        }
    }
 
    return true;
}
const char* cmd1060[] = {"state", "lumen", "priority", "$", "$", "$", "$"};
Command cmd_state_lumen_set_priority(
    cmd1060,
    ELEMENTS_OF(cmd1060),
    "Set the relative priority of the illumination states",
    *f_state_lumen_set_priority,
    CommandList);



bool f_state_lumen_priority_print(Command* p_command, String& p_output)
{
    return Lumen_State.print_priority(p_output);
}
const char* cmd1070[] = {"state", "lumen", "priority", "print"};
Command cmd_state_lumen_priority_print(
    cmd1070,
    ELEMENTS_OF(cmd1070),
    "Print the relative priority of the illumination states, highest priority first",
    *f_state_lumen_priority_print,
    CommandList);



// The Lumen_Level indicates the brightness of the Semaphore Light,
// 1=dim and 9=bright
char Lumen_Level = '5';

bool f_state_lumen_level_set(Command* p_command, String& p_output)
{
    const char* level = p_command->get_macro(0);
    if (!level)
    {
        p_output = "Error: Missing parameter";
        return false;
    }

    if ((level[0] < '1') || (level[0] > '9'))
    {
        p_output = "Error: Invalid parameter";
        return false;
    }

    p_output = level[0];
    return true;
}
const char* cmd2000[] = {"state", "lumen", "level", "set", "$"};
Command cmd_state_lumen_level_set(
    cmd2000,
    ELEMENTS_OF(cmd2000),
    "Set the illumincation intensity level, 1-9, where 9 is highest",
    *f_state_lumen_level_set,
    CommandList);



bool f_state_lumen_level_print(Command* p_command, String& p_output)
{
    p_output = Lumen_Level;
    return true;
}
const char* cmd2010[] = {"state", "lumen", "level", "print"};
Command cmd_state_lumen_level_print(
    cmd2010,
    ELEMENTS_OF(cmd2010),
    "Print the illumination intensity level, 1-9, where 9 is highest",
    *f_state_lumen_level_print,
    CommandList);



#if 0
state request red - Request sempahore enter red state
state release red - Relinguish red state request
state request yellow - Request sempahore enter yellow state
state release yellow - Relinquish red state request
state request green - Request sempahore enter green state
state release green - Relinquish green state request
state release all - Relinquish all state requests, return to default state
state print - Print the current state of this semaphore
state log - Print audit log of state transitions
cfg state default red - Set semaphore state to red if no other state requests
cfg state default yellow - Set semaphore state to yellow if no other state requests
cfg state default green - Set semaphore state to green if no other state requests
cfg state log depth - Set maximum number of lines to keep in state log

cfg move lumen off - Turn off illumination while moving semaphore
cfg move lumen on - Turn on illumination while moving semaphore
cfg move lumen blink slow - Blink illumination slowly while moving semaphore
cfg move lumen blink fast - Blink illumination fast while moving semaphore

cfg move slow - move semaphore slowly
cfg move fast - move semaphore quickly

cfg lumen {1-9} - illumination intensity, 1 is lowest, 9 is highest

Notifications
Notify target when moved to the indicated position, Repeat this config as needed
cfg notify (when pr,send cr,to ipv4 addr 192.168.x.y)

Network
cfg ipv4 addr 192.168.100.1 - Network Address of the device
cfg ipv4 mask 255.255.255.0 Network mask
cfg wifi ssid LiveSteam - The WiFi SSID to connect with
cfg wifi pass superheater The password of the wifi network
#endif

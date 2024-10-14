#
# Class for loading and encapsulating signal configuration for SigOS
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

import io
import json
import Head
import Semaphore
import Light

class Config:

    # Class variable - singleton for the configuration
    c_config = None

    # Create an object to encapsulate configuraton for the signal
    # @param p_file Filename of a json config file
    #
    def __init__(self, p_file):
        # Read the json file and parse
        self.m_file = p_file
        fs = io.open(p_file, 'r')
        config = json.load(fs)
        fs.close()

        self.m_board_type = config["board-type"]
        self.m_hostname = config["hostname"]
        self.m_wifi_ssid = config["wifi-ssid"]
        self.m_wifi_password = config["wifi-password"]
        self.m_ip_addr = config["ip-addr"]
        self.m_light_on_approach = config["light-on-approach"] == "true"
        self.m_number_plate = config["number-plate"] == "true"
        self.m_rules_file = config["rules-file"]
        self.m_semaphore_count = 0
        self.m_ligth_count = 0

        # Remove ".local" from hostname, if present
        hostname_list = self.m_hostname.split(".")
        self.m_hostname = hostname_list[0]

        # Build heads object
        heads = config["heads"]
        self.m_head_array = list()
        for head in heads:
            head_id = head["head-id"]
            head_obj = Head.Head(head_id)

            if ("lights" in head):
                lights_list = head["lights"]
                for light in lights_list:
                    light_id = light["light-id"]
                    ws281_id = light["ws281-id"]
                    colors = light["colors"]
                    light_obj = Light.Light(head_id, light_id, colors)
                    head_obj.add_light(light_obj)
                    self.m_light_count += 1
            elif ("semaphores" in head):
                semaphore_list = head["semaphores"]
                for semaphore in semaphore_list:
                    semaphore_id = semaphore["semaphore-id"]
                    degrees_per_second = semaphore["degrees-per-second"]
                    semaphore_obj = Semaphore.Semaphore(head_id, semaphore_id, degrees_per_second)
                    head_obj.add_semaphore(semaphore_obj)
                    self.m_semaphore_count += 1
            else:
                self.m_log.add(p_source, "Invalid fixture in config 202410112120");

            self.m_head_array.append(head_obj)

        # Load the WS281 color chart
        self.m_color_chart = config["color-chart"]

        # Save this singleton
        Config.c_config = self


    # @returns The number of heads configured for this signal
    #
    def head_count(self):
        return len(self.m_head_array)


    # @returns The number of semaphores configured for this signal
    #
    def semaphore_count(self):
        return self.m_semaphore_count


    # @returns The number of lights configured for this signal
    #
    def light_count(self):
        return self.m_light_count


    # @returns True if this signal has a number plate
    #
    def number_plate(self):
        return self.m_number_plate


    # @returns A string representation of this rule set
    #
    def __str__(self):
        s = "board-type: "
        s += self.m_board_type
        s = "hostname: "
        s += self.m_hostname
        s += "\nip-addr: "
        s += self.m_ip_addr
        s += "\nlight-on-approach: "
        s += str(self.m_light_on_approach)
        s += "\nnumber-plate: "
        s += self.m_number_plate
        s += "\nrules_file: "
        s += self.m_rules_file
        s += "\n"
        for head in self.m_head_array:
            s += str(head)
        return s


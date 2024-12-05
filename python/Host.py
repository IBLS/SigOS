#
# Class to maintain mapping between Hostname and IP address
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

import usocket

class Host:

    # Class variable to hold list of registered Hosts
    c_hosts = list()

    # Create an object to map a Hostname to an IP address
    # Do not call directly, call Register_Host() instead.
    # @param p_hostname The string hostname. MicroPython mDNS limits to 32 characters.
    # @param p_ip The IPv4 address associated with p_hostname. If "None" then
    #             attempt to resolve using mDNS or DNS.
    #
    def __init__(self, p_hostname, p_ip):
        self.m_hostname = p_hostname
        self.m_ip = p_ip
        Host.c_hosts.append(self)


    # Register a Hostname to IP address mapping
    # @param p_hostname The string hostname. MicroPython mDNS limits to 32 characters.
    # @param p_ip The IPv4 address associated with p_hostname. If "None" then
    #             attempt to resolve using mDNS or DNS.
    # @returns True on success, False if unable to resolve hostname or other error.
    #
    @classmethod
    def Register_Host(p_class, p_hostname, p_ip):
        ip = p_ip
        if ip is None:
            # Try to resolve hostname using mDNS or DNS
            # Result looks like this:
            # [(2, 1, 0, 'onvakkiock.local', ('192.168.1.66', 80))]
            try:
                info = usocket.getaddrinfo(p_hostname, 23, 0, usocket.SOCK_STREAM)
                data = info[0]
                ip_port = data[4]
                ip = ip_port[0]
            except OSError:
                # Could not resolve p_hostname
                return False

        # See if the hostname is already registered
        for host in p_class.c_hosts:
            if p_hostname == host.m_hostname:
                if ip != self.m_ip:
                    # Update the mapping to use the new IP address
                    self.m_ip = ip
                return True

        # Create and add new hostname/ip entry
        Host(p_hostname, ip)
        return True 


    # Find the IP address that matches the given Hostname
    # from the previously registered list.
    # @param p_class This class
    # @param p_hostname The hostname to lookup.
    # @returns The associated IP address, or None if no match.
    #
    @classmethod
    def GetIP(p_class, p_hostname):
        for host in p_class.c_hosts:
            if p_hostname == host.m_hostname:
                return host.m_ip
        return None


    # Find the Hostname that matches the given IP Address
    # from the previously registered list.
    # @param p_class This class
    # @param p_ip The IP Address to lookup.
    # @returns The associated Hostname, or None if no match.
    #
    @classmethod
    def GetHostname(p_class, p_ip):
        for host in p_class.c_hosts:
            if p_ip == host.m_ip:
                return host.m_hostname
        return None

    # @returns A string representation of this rule set
    #
    def __str__(self):
        s = "host: "
        s += self.m_hostname
        s += " ip: "
        s += self.m_ip
        return s


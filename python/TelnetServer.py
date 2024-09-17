#
# Classes for implementing Telnet Servers
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

# Adapted from
#  https://github.com/cpopp/MicroTelnetServer/blob/master/utelnet/utelnetserver.py

import socket
import network
import uos
import errno
from uio import IOBase 

# Provide necessary functions for dupterm and replace telnet control characters that come in.

class TelnetConn(IOBase):
    
    # Class variables
    c_wrapper_list = list()


    # Initialize instance variable for a new object
    # @param p_client_socket A socket object for read/writing to the attached client
    # @param p_client_addr The IP address of the attached client
    # @param p_client_port The port number of the attached client
    #
    def __init__(self, p_client_socket, p_client_addr, p_client_port):
        self.m_client_socket = p_client_socket
        self.m_client_addr = p_client_addr
        self.m_client_port = p_client_port

        self.m_discard_count = 0
        self.m_state = 0
        TelnetConn.c_wrapper_list.append(self)

        self.m_client_socket.setblocking(False)
        self.m_client_socket.sendall(bytes([255, 252, 34])) # dont allow line mode
        self.m_client_socket.sendall(bytes([255, 251, 1])) # turn off local echo

        self.write("Welcome ")
        self.write(str(self.m_client_addr))
        self.write(":")
        self.write(str(self.m_client_port))
        self.write("!\r\n")

        #self.start_repl()


    # Connect the MicroPython terminal (the REPL) to the client socket
    #
    def  start_repl(self):
        # dupterm_notify() not available under MicroPython v1.1
        # self.m_client_socket.setsockopt(socket.SOL_SOCKET, 20, uos.dupterm_notify)
        uos.dupterm(self.m_client_socket, 0)


    # Disconnect the REPL from the  client socket
    #
    def stop_repl(self):
        uos.dupterm(None, 0)


    # Read characters (if any) into p_buffer
    # @param p_buffer A memory buffer to receive characters into
    # @returns The number of bytes read into p_buffer, or None
    # 
    def readinto(self, p_buffer):
        readbytes = 0
        for i in range(len(p_buffer)):
            try:
                byte = 0
                # discard telnet control characters and
                # null bytes 
                byte = self.socket.recv(1)[0]

            except (OSError) as e:
                if len(e.args) > 0 and e.args[0] == errno.EAGAIN:
                    # No more bytes in the socket, return and try again later
                    if (readbytes == 0):
                        return None
                    return readbytes
                else:
                    # Some other error?
                    raise

            if (self.m_state == 0):
                # discard telnet control characters and
                # null bytes 
                if (byte == 0):
                    self.m_discard_count += 1
                    continue
                if (byte == 0xFF):
                    self.m_state = 1
                    self.m_discard_count += 1
                    continue

            if (self.m_state == 1):
                # Discard this control character
                self.m_discard_count += 1
                self.m_state = 0
                continue

            # Add character to p_buffer
            p_buffer[i] = byte
            readbytes += 1

        return readbytes


    # Write bytes into the stream 
    # @param p_buffer A string of one or more characters
    # @returns The number of bytes written
    #
    def write(self, p_buffer):
        bytes_out = 0
        while (len(p_buffer) > 0):
            try:
                written_bytes = self.m_client_socket.write(p_buffer)
                bytes_out += written_bytes
                p_buffer = p_buffer[written_bytes:]
            except OSError as e:
                if len(e.args) > 0 and e.args[0] == errno.EAGAIN:
                    # Can't write yet, try again later
                    return bytes_out
                else:
                    # Something else...propagate the exception
                    raise

        return bytes_out


    # Close the connection
    # 
    def close(self):
        stop_repl()
        if (self.m_socket):
            self.m_socket.close()
        self.m_socket = None


    # Destructor
    #
    def __del__(self):
        self.close()


class TelnetServer:

    # Class variables
    c_server_port = list()
    c_server_socket = list()

    # Initialize instance variables
    #
    def __init__(self):
        self.m_server_socket = None


    # Listening for telnet connections on port 23
    # @param p_port The port number of the server service, default 23
    # @param p_backlog The number of unaccepted connections allowed before refusing new conns
    # @returns True on success, False on failure
    #
    def start(self, p_port=23, p_backlog=4):
        # Make sure the service is not already established
        for i in TelnetServer.c_server_port:
            if (TelnetServer.c_server_port[i] == p_port):
                return False

        self.m_server_port = p_port
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Register with the class
        TelnetServer.c_server_port.append(p_port)
        TelnetServer.c_server_socket.append(server_socket)
        if (len(TelnetServer.c_server_port) != len(TelnetServer.c_server_socket)):
            # Something went wrong
            return False

        # Get my ip address
        ai = socket.getaddrinfo("0.0.0.0", p_port)
        addr = ai[0][4]
        
        server_socket.bind(addr)
        server_socket.listen(p_backlog)

        # Register a callback function for accepting new connections
        server_socket.setsockopt(socket.SOL_SOCKET, 20, cb_accept_telnet_connect)

        # Report if the server was started on an AP, Station, or both
        for i in (network.AP_IF, network.STA_IF):
            wlan = network.WLAN(i)
            if wlan.active():
                print("Telnet server started on {}:{}".format(wlan.ifconfig()[0], p_port))
                return True

        # Failed to connect to server
        return False

 
    # Close all server ports
    #
    def stop(self):
        for i in c_server_socket:
            c_server_socket[i].close()


# Attach new clients to dupterm and 
# send telnet control characters to disable line mode
# and stop local echoing
# @returns A ClientWrapper for reading and writing
#
def cb_accept_telnet_connect(p_server_socket):

    client_socket, client_addr_port = p_server_socket.accept()
    client_addr = client_addr_port[0]
    client_port = client_addr_port[1]
    print("Telnet connection from:", client_addr, ":", client_port)

    # Create a new TelnetConn object
    TelnetConn(client_socket, client_addr, client_port)



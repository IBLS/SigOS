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
import select
import uos
import errno
from uio import IOBase 
import Log
import Command

class TelnetConn(IOBase):
    
    # Class variables
    c_client_list = list()
    c_input_buffer = bytearray(512)

    # Initialize instance variable for a new object
    # @param p_client_socket A socket object for read/writing to the attached client
    # @param p_client_addr The IP address of the attached client
    # @param p_client_port The port number of the attached client
    # @param p_welcome The welcome message to print at the start of each client session
    #
    def __init__(self, p_client_socket, p_client_addr, p_client_port, p_welcome):
        self.m_client_socket = p_client_socket
        self.m_client_addr = p_client_addr
        self.m_client_port = p_client_port
        self.m_to_discard = 0

        TelnetConn.c_client_list.append(self)

        self.m_client_socket.setblocking(False)
        #self.m_client_socket.sendall(bytes([255, 252, 34])) # dont allow line mode
        #self.m_client_socket.sendall(bytes([255, 251, 1])) # turn off local echo

        # Send initial prompt
        if (p_welcome):
            self.write(p_welcome)

        self.prompt()

        #self.start_repl()


    # Connect the MicroPython terminal (the REPL) to the client socket
    #
    def  start_repl(self):
        uos.dupterm(self.m_client_socket, 0)


    # Disconnect the REPL from the  client socket
    #
    def stop_repl(self):
        uos.dupterm(None, 0)


    # Read characters (if any) into p_buffer
    # @param p_buffer A memory buffer to receive characters into
    # @returns The number of bytes read into p_buffer
    # 
    def readinto(self, p_buffer):
        readbytes = 0
        for i in range(len(p_buffer)):
            try:
                byte = 0
                while (byte == 0):
                    byte = self.m_client_socket.recv(1)[0]

                    # discard telnet control characters and null bytes 
                    if byte == 0:
                        continue

                    if byte == 0xFF:
                        self.m_to_discard = 2
                        byte = 0
                        continue

                    if self.m_to_discard > 0:
                        self.m_to_discard -= 1
                        byte = 0
                        continue

                p_buffer[i] = byte
                readbytes += 1

            except (IndexError, OSError) as e:
                if type(e) == IndexError or len(e.args) > 0 and e.args[0] == errno.EAGAIN:
                    # No more bytes in the socket, return and try again later
                    return readbytes
                elif type(e) == OSError and len(e.args) > 0:
                    if e.args[0] == errno.ECONNABORTED or e.args[0] == errno.ECONNRESET or e.args[0] == errno.ENOTCONN:
                        # Close this connection
                        self.close()
                        return 0
                    else:
                        # Some other error?
                        raise
                else:
                    # Some other error?
                    raise

        return readbytes


    # Write bytes into the stream 
    # @param p_buffer A string of one or more characters
    # @returns The number of bytes written
    #
    def write(self, p_buffer):
        if (not self.m_client_socket):
            return 0
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



    # Print a prompt on the terminal
    #
    def prompt(self):
        self.write("> ")


    # Poll will check for messages from the Telnet Client and
    # execute commands as requested
    #
    @classmethod
    def Poll(p_class):
        # Check for traffic from each Telnet clinet
        client_list = p_class.c_client_list
        for client in client_list:
            len = client.readinto(p_class.c_input_buffer)
            # Get the string name of Telnet client (usually its IP address)
            source = str(client.m_client_addr)
            # print("len=", len)
            keeplinebreaks = False
            lines = p_class.c_input_buffer[0:len].splitlines(keeplinebreaks)
            for line in lines:
                # Convert binary buffer to string
                line_decoded = line.decode()
                # Attempt to parse and execute the specified command line
                # print(line)
                (cmd_match, func_result, result_list) = Command.Command.ParseAndExec(line_decoded, source)
                if (not cmd_match):
                    pass
                if (not func_result):
                    result_list.append('Command failed')
                for out_line in result_list:
                    try:
                        client.m_client_socket.write(out_line)
                        client.m_client_socket.write("\r\n")
                    except Exception as e:
                        # Log the error
                        pass
                client.prompt()


    # Close the connection
    # 
    def close(self):
        TelnetConn.c_client_list.remove(self)
        if (self.m_client_socket):
            self.stop_repl()
            self.m_client_socket.close()
        self.m_client_socket = None


    # Destructor
    #
    def __del__(self):
        self.close()


g_welcome = None

class TelnetServer:

    # Class variables
    c_server_port = list()
    c_server_socket = list()

    # Initialize instance variables
    #
    def __init__(self):
        self.m_server_socket = None


    # Set the welcome message printed at the start of each client session
    # @param p_welcome The welcome message to print at the start of each client session
    #
    def set_welcome(self, p_welcome):
        global g_welcome
        g_welcome = p_welcome


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

        # Setup poller
        self.m_poller = select.poll()
        self.m_poller.register(server_socket, select.POLLIN)

        # Report if the server was started on an AP, Station, or both
        for i in (network.AP_IF, network.STA_IF):
            wlan = network.WLAN(i)
            if wlan.active():
                print("Telnet server started on {}:{}".format(wlan.ifconfig()[0], p_port))
                return True

        # Failed to connect to server
        return False


    # Poll the socket for input
    # @returns True if input was ready
    #
    def poll(self):
        res = self.m_poller.poll(10)
        return res

 
    # Close all server ports
    #
    def stop(self):
        for i in c_server_socket:
            c_server_socket[i].close()

    # Close the specified client
    # @param p_client_name The hostname or IP address string of the client to close.
    # @returns True on success, false if client not found
    #
    @classmethod
    def Close(p_class, p_client_name):
        for client in TelnetConn.c_client_list:
            client_name = str(client.m_client_addr)
            if client_name == p_client_name:
                client.close()
                return True
        return False


# Attach new clients to dupterm and 
# send telnet control characters to disable line mode
# and stop local echoing
# @returns A ClientWrapper for reading and writing
#
def cb_accept_telnet_connect(p_server_socket):

    client_socket, client_addr_port = p_server_socket.accept()
    client_addr = client_addr_port[0]
    client_port = client_addr_port[1]

    # Create a new TelnetConn object
    try:
        TelnetConn(client_socket, client_addr, client_port, g_welcome)
    except:
        return

    log = Log.Log()
    log.add(str(client_addr), "Client connection")


/*
 * Command Processor for SigOS
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
#ifndef _TCP_Server_h_
#define _TCP_Server_h_

#ifdef __linux__
#include <assert.h>
#include "os_compat.h"
#include "Endpoint.h"
#else
#include "os_compat.h"
#include <Endpoint.h>
#endif

class TCP_Server
{
  public:
    TCP_Server(int p_server_port = 23, bool p_echo = true) :
        m_server(NULL),
        m_server_port(p_server_port),
        m_echo(p_echo)
    {
    }

    ~TCP_Server()
    {
        delete m_server;
    }

    /// Call this method to start a new TCP Server.
    ///
    bool begin(void)
    {
        assert(m_server == NULL);
        m_server = new Endpoint(m_server_port);
        if (!m_server)
        {
            return false;
        }

        m_server->begin();
        return true;
    }


    /// Get a command string from a client, if any.
    /// \param p_command Reference to the string that receives the command.
    /// \returns The Endpoint along with the command in p_command,
    ///          or returns a Null Endpoint if not commands.
    ///
    Endpoint* get_command(String& p_command)
    {
        // Get the next client with data to read
        Endpoint* client = m_server->available();
        if (client)
        {
            // Get the next line
            p_command = client.readStringUntil('\n');

            if (m_echo)
            {
                // Echo back to telnet user
                client.print(p_command);
                client.flush();
            }

            // Trim carriage return
            p_command.trim();
        }

        return client;
    }


    /// Send the given message to all connected clients
    /// \param p_msg The message to send to all connected clients.
    /// \returns True on success, false if the server has not started.
    ///
    bool send_all(String& p_msg)
    {
        if (!m_server)
        {
            return false;
        }

        m_server->print(p_msg);
        m_server->flush();
        return true;
    }

  private:
    Endpoint*           m_server;
    int                 m_server_port;
    bool                m_echo;
};

#endif // _TCP_Server_h


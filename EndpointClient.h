/*
   Command Processor for SigOS

   Copyright (C) 2021 Daris A Nevil - International Brotherhood of Live Steamers

   Permission is hereby granted, free of charge, to any person obtaining a
   copy of this software and associated documentation files (the "Software"),
   to deal in the Software without restriction, including without limitation
   the rights to use, copy, modify, merge, publish, distribute, sublicense,
   and/or sell copies of the Software, and to permit persons to whom the
   Software is furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included
   in all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
   DARIS A NEVIL, OR ANY OTHER CONTRIBUTORS BE LIABLE FOR ANY CLAIM,
   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
   OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
   OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

*/
#ifndef _EndpointClient_h_
#define _EndpointClient_h_

#ifdef __linux__

class EndpointClient
{
  private:

    int      m_server_port;

  public:
    EndpointClient(int p_server_port) : m_server_port(p_server_port)
    {
    }

    bool begin(void)
    {
      return false;
    }

    EndpointClient* available(void)
    {
      return NULL;
    }
};

#else
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
typedef WiFiClient EndpointClient;

#if 0
class EndpointClient : public WiFiClient
{
};
#endif

#endif


#endif // _EndpointClient_h

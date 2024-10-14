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
#ifdef __linux__

#include "TCP_Server.h"
#include <ESP8266WiFi.h>
#include <WiFiUDP.h>
#include <FS.h>
#include <IBLS_Semaphore.h>
#include <Array.h>
#include <NTPClient.h>
#include <TCP_Server.h>

TCP_Server telnet;

WiFiUDP ntpUDP;
// Default to 'pool.ntp.org', 60 second update interval, no offset (GMT)
NTPClient timeClient(ntpUDP);
unsigned long Now(void)
{
   return timeClient.getEpochTime();
}


void setup() {
  
  // Initialize the serial port
  delay(1000);
  Serial.begin(115200);
  delay(1000);
  Serial.print("\n");

  Serial.println("Connecting to wifi...\n");
  WiFi.begin("IGNRR", "downcase");
  while (WiFi.status() != WL_CONNECTED)
  {
      delay(500);
      Serial.print('.');
  }

  Serial.print("\nConnected to ");
  Serial.println(WiFi.SSID());
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Init NTP Client
  timeClient.begin();
  
  String help;
  Help(help);
  Serial.println(help);

  // Initialize I/O pins
  // power_up_pinmode();

  // Start the telnet server
  bool result = telnet.begin();
  assert(result);
}

void loop() {
  // put your main code here, to run repeatedly:

  // Update from ntp
  timeClient.update();
  Serial.println(timeClient.getFormattedTime());
  Serial.println(timeClient.getEpochTime());

  // Get telnet command, if any
  String telnet_command;
  Endpoint client = telnet.get_command(telnet_command);
  if (client)
  {
      ProcessCommand(client, telnet_command);
  }

  delay(1000);                       // wait for a second
  Serial.println("Waiting");
}

#endif // __linux__

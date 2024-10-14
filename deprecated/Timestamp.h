/*
 * General timestamp class
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
#ifndef _Timestamp_h_
#define _Timestamp_h_

#include <Arduino.h>
#include <string.h>
//#include <Array.h>
#include <assert.h>


// The Now() function must be defined in the main cpp file
extern unsigned long Now(void);

class Timestamp
{
  public:
    Timestamp() :
        m_now(Now()),
        m_millis(millis() % (86400 * 1000))
    {
    }


    /// Create a string representing the time.
    /// Copied from NTPClient
    ///
    bool print(String& p_string) const
    {
        unsigned long hours = (m_now % 86400L) / 3600;
        String hoursStr = hours < 10 ? "0" + String(hours) : String(hours);

        unsigned long minutes = (m_now % 3600) / 60;
        String minuteStr = minutes < 10 ? "0" + String(minutes) : String(minutes);

        unsigned long seconds = m_now % 60;
        String secondStr = seconds < 10 ? "0" + String(seconds) : String(seconds);

        p_string += hoursStr + ":" + minuteStr + ":" + secondStr;
        return true;
    }


  public:
    time_t          m_now;
    unsigned long   m_millis;
};

#endif // _Timestamp_h_

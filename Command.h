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
#ifndef _Command_h_
#define _Command_h_

#include "EndpointClient.h"
#include <string.h>
#include "Array.h"
#include <assert.h>
#include <IPAddress.h>
#include "Timestamp.h"


// Forward declaration
class Command;

typedef bool (*Command_Func_t)(Command* p_command, String& p_output);
typedef Array<Command*> CommandList_t;

extern bool ProcessCommand(EndpointClient p_client, String& p_command);

class Command
{
  public:
	Command(
        const char** p_words,
        size_t p_words_len,
        const char* p_desc,
        Command_Func_t p_func,
        CommandList_t& p_command_list) :
            m_words(p_words),
            m_words_len(p_words_len),
            m_desc(p_desc),
            m_func(p_func)
	{
        // Add myself to the CommandList
        p_command_list.push_back(this);
    }

    ~Command()
    {
    }

    /// Compare the input to the command, and if a match, execute the associated function.
    /// \param p_words An array of input words.
    /// \param p_words_len The number of strings in p_words.
    /// \param p_func_result The result of the function, if called
    /// \param p_output Reference to a string to receive user-text from the command.
    /// \returns True if the command matches and the function was executed, false otherwise.
    ///
    bool parse_and_exec(
        const char** p_words,
        size_t p_words_len,
        bool& p_func_result,
        String& p_output,
        Timestamp p_timestamp,
        IPAddress p_source_ip)
    {
        m_timestamp = p_timestamp;
        m_source_ip = p_source_ip;

        if (p_words_len != m_words_len)
        {
            return false;
        }

        for (size_t i = 0; i < p_words_len; ++i)
        {
            if ((m_words[i])[0] == '$')
            {
                // Let m_func expand the macro, if called
                m_macros.push_back(p_words[i]);
                continue;
            }

            if (strcmp(p_words[i], m_words[i]) != 0)
            {
                return false;
            }
        }

        // Execute the function and provide the return value
        p_func_result = (*m_func)(this, p_output);

        // The command matched
        return true;
    };

    /// Build text that describes this command
    /// \param p_help Reference to a string to receive the help text.
    ///
    void help(String& p_help) const
    {
        bool first = true;
        for (size_t i = 0; i < m_words_len; ++i)
        {
            if (first)
            {
                first = false;
            }
            else
            {
                p_help += " ";
            }

            p_help += m_words[i];
        }

        p_help += " : ";
        p_help += m_desc;
        p_help += "\n";
    }


    /// Get the specified macro parameter.
    /// \paramp_macro_index The zero-based index number of the input macro
    /// \returns A pointer to the specified input macro, or NULL
    ///
    const char* get_macro(size_t p_macro_index)
    {
        if (p_macro_index >= m_macros.size())
        {
            return NULL;
        }

        return m_macros[p_macro_index];
    }


    /// \returns The timestamp when the command was received.
    ///
    Timestamp get_timestamp(void)
    {
        return m_timestamp;
    }


    /// \returns The IP Address of the command issuer.
    ///
    IPAddress get_source_ip(void)
    {
        return m_source_ip;
    }

  private:
    const char**	    m_words;
    size_t              m_words_len;
    const char*         m_desc;
    Command_Func_t      m_func;
    Array<const char*>  m_macros;
    Timestamp           m_timestamp;
    IPAddress           m_source_ip;
};


#endif // _Command_h_

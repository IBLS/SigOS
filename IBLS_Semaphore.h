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
#ifndef _IBLS_Semaphore_h_
#define _IBLS_Semaphore_h_

#include <assert.h>
#include <string.h>
#include <Arduino.h>
#include "Array.h"
#include <IPAddress.h>
#include "Timestamp.h"
#include "Command.h"


// Compute the number of elements in a constant array
#define ELEMENTS_OF(x) (sizeof(x) / sizeof((x)[0]))

void power_up_pinmode(void);

// Forward Decl
//class Command;

void Help(String& p_help);



class NV_Var
{
};



class StateRequest
{
  public:
    StateRequest(
        int p_state_request,
        IPAddress& p_source,
        Timestamp& p_timestamp)
        :
        m_state_request(p_state_request),
        m_source(p_source),
        m_timestamp(p_timestamp)
    {
    }

    // Copy constructor
    StateRequest(const StateRequest& p_copy) :
        m_state_request(p_copy.m_state_request),
        m_source(p_copy.m_source),
        m_timestamp(p_copy.m_timestamp)
    {
    }

    StateRequest() :
        m_state_request(-1),
        m_source(IPAddress(0,0,0,0))
    {
    }

    /// Compare this StateRequest to another. Don't use the timestamp in the comparison.
    /// \param p_rhs The other StateRequest on the right hand side of ==
    /// \returns True if the StateRequests match
    ///
    bool operator==(StateRequest& p_rhs)
    {
        return (m_state_request == p_rhs.m_state_request) &&
               (m_source == p_rhs.m_source);
    }


    /// \returns The requested state
    ///
    int get_state(void) const
    {
        return m_state_request;
    }


    /// Print the State Request.
    /// \param p_string Reference to a string to receive the State Request.
    ///
    bool print(String& p_string, const char** p_state_names)
    {
        // Print timestamp
        m_timestamp.print(p_string);
        p_string += ": ";

        // Print state name
        p_string += p_state_names[m_state_request];
        p_string += ", ";

        // Print IP address of requestor
        p_string += m_source.toString();

        return true;
    }

  public:
    int             m_state_request;
    IPAddress       m_source;
    Timestamp       m_timestamp;
};


class StateMgr
{
  public:

    StateMgr(const char** p_state_names, size_t p_state_count) :
        m_state_count(p_state_count),
        m_state_names(p_state_names),
        m_default_state(0)
    {
        m_state_priority = new int[p_state_count];
        assert(m_state_priority);

        // Initialize priority array
        for (size_t i = 0; i < sizeof(m_state_priority); ++i)
        {
            // Assume simple priority based on value of the enum
            m_state_priority[i] = i;
        }
    }


    /// Set the default state, which will become the current active state when there
    /// are no active state requests.
    /// \param p_default_state The default state.
    ///
    void set_default_state(int p_default_state)
    {
        m_default_state = p_default_state;
    }


    /// \returns The default state.
    ///
    int get_default_state(void) const
    {
        return m_default_state;
    }


    /// \returns The string name of the default state.
    ///
    const char* get_default_name(void) const
    {
        return m_state_names[m_default_state];
    }


    /// Set the current priority of the 
    /// \param p_state The state that will receive a new priority
    /// \param p_priority The new priority to assign to p_state
    ///
    void set_priority(int p_state, int p_priority)
    {
        assert(p_state < sizeof(m_state_priority));
        m_state_priority[p_state] = p_priority;
    }


    /// \param p_state The state requesting the priority
    /// \returns The priority of the given state
    ///
    int get_priority(int p_state)
    {
        assert(p_state < sizeof(m_state_priority));
        return m_state_priority[p_state];
    }


    /// Print the priority of states, with the highest priority
    /// at the first of the list.
    /// \param p_string Reference to a string to receive the list of names
    /// \returns True on success
    ///
    bool print_priority(String& p_string)
    {
        for (size_t pri = 0; pri < m_state_count; ++pri)
        {
            for (size_t state = 0; state < m_state_count; ++state)
            {
                if (m_state_priority[state] == pri)
                {
                    p_string += " ";
                    p_string += m_state_names[state];
                    break;
                }
            }
        }

        return true;
    }


    /// Register a new active state request
    /// \param p_request The request object holding the who, what and when
    /// \returns True if this is a new state, false if it already exists
    ///
    bool request_state(StateRequest& p_request)
    {
        for (size_t i = 0; i < m_active_states.size(); ++i)
        {
            if (m_active_states[i] == p_request)
            {
                // This request already exists
                return false;
            }
        }

        bool result = m_active_states.push_back(p_request);
        assert(result);
        return true;
    }

    /// Remove an active state request. Only removes a request by the specified sender.
    /// \param p_release The active state to be released
    /// \returns True if the state was found in the request list, false otherwise
    ///
    bool release_state(StateRequest& p_release)
    {
        // Find the state, if it exists
        for (size_t i = 0; i < m_active_states.size(); ++i)
        {
            if (m_active_states[i] == p_release)
            {
                // Remove the state from the array
                m_active_states.remove(i);
                return true;
            }
        }

        // State not found
        return false;
    }


    /// Remove all matching state requrests, regardless of the requestor.
    /// \param p_release The active state to be released
    /// \returns True if the state was found in the request list, false otherwise
    ///
    bool release_state_all(int p_state)
    {
        // Find the state, if it exists
        for (size_t i = 0; i < m_active_states.size(); ++i)
        {
            if (m_active_states[i].get_state() == p_state)
            {
                // Remove the state from the array
                m_active_states.remove(i);
                return true;
            }
        }

        // State not found
        return false;
    }

    /// Remove all active states
    ///
    void reset_state(void)
    {
        m_active_states.clear();
    }


    /// Review all state requests currently active and determine which
    /// state has the highest priority (e.g. this is the current active state).
    /// \returns The current active state. If not active requests then the
    ///          default state is returned.
    ///
    int get_priority_state(void)
    {
        int current_state = m_default_state;
        int current_priority = 0;

        // Find state requests
        for (size_t i = 0; i < m_active_states.size(); ++i)
        {
            int requested_state = m_active_states[i].get_state();
            int requested_priority = m_state_priority[requested_state];

            if (requested_priority > current_priority)
            {
                current_priority = requested_priority;
                current_state = requested_state;
            }
        }

        return current_state;
    }


    /// Print the State Request.
    /// \param p_string Reference of a string to receive the list of
    ///        active state requests.
    ///
    bool print(String& p_string)
    {
        for (size_t i = 0; i < m_active_states.size(); ++i)
        {
            m_active_states[i].print(p_string, m_state_names);
            p_string += "\n";
        }

        if (m_active_states.empty())
        {
            p_string += "No active requests\n";
        }

        int priority_state = get_priority_state();
        p_string += "Current state: ";
        p_string += m_state_names[priority_state];
        p_string += "\n";

        return true;
    }

  private:
    Array<StateRequest>     m_active_states;

    // Number of states
    size_t                  m_state_count;

    // Pointer to the printable state names
    const char**            m_state_names;

    // This is the default state
    int                     m_default_state;

    // Make a state priority array the same size of name array
    int*                    m_state_priority;
};


#endif // _IBLS_Semaphore_h_

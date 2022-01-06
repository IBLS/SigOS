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
#ifndef __Array_h_
#define __Array_h_

#include <Arduino.h>
#include <assert.h>

template <class Type>
class Array
{
  public:
    Array<Type>() :
        m_vector(NULL),
        m_vector_elems(0),
        m_vector_max(0)
    {
    }

    ~Array<Type>()
    {
        delete [] m_vector;
    }


    /// Assign the contents of another array to this one by copying elements.
    /// \param p_array Reference to another Array of the same type.
    /// \returns False on error (such as no memory)
    ///
    bool assign(Array<Type>& p_array)
    {
        size_t new_size = p_array.size();
        clear();
        if (!reserve(new_size))
        {
            return false;
        }
        for (size_t i = 0; i < new_size; ++i)
        {
            m_vector[i] = p_array.m_vector[i];
        }
        return true;
    }

    /// Assign the contents of a constant C array to this one by copying elements.
    /// \param p_array Pointer to a constant array of the same type.
    /// \param p_array_size Number of elements in the constant array.
    ///
    void assign(const Type* p_array, size_t p_array_size)
    {
        clear();
        if (!reserve(p_array_size))
        {
            return false;
        }
        for (size_t i = 0; i < p_array_size; ++i)
        {
            m_vector[i] = p_array->m_vector[i];
        }
        return true;
    }

    /// Assign a single element of the same type to this Array.
    ///
    void assign(Type& p_elem)
    {
        clear();
        if (!reserve(1))
        {
            return false;
        }
        m_vector[0] = p_elem;
        return true;
    }

    /// Access an element in the array.
    /// \param p_index The zero-based index number of the element to access
    /// \returns A pointer to the Array slot
    ///
    Type& at(size_t p_index)
    {
        assert(p_index < m_vector_elems);
        return m_vector[p_index];
    }
    Type& operator[](size_t p_index)
    {
        assert(p_index < m_vector_elems);
        return m_vector[p_index];
    }

    /// \returns A pointer to the last element in the Array.
    ///
    Type& back(void)
    {
        assert(!empty());
        return m_vector[m_vector_elems-1];
    }

    /// \returns A pointer to the first element in the Array.
    ///
    Type& front(void)
    {
        assert(!empty());
        {
            return NULL;
        }
        return &m_vector[0];
    }

    /// \returns The size of the storage space currently allocated to the Array.
    ///
    size_t capacity(void) const
    {
        return m_vector_max;
    }

    /// Removes all elements from the vector, leaving the container with a size of 0.
    ///
    void clear(void)
    {
        // Don't delete m_vector
        m_vector_elems = 0;
    }

    /// \returns A direct pointer to the memory array used internally by the vector.
    ///          Please note this pointer can later become invalidated by further operations
    ///          on the Array.
    ///
    Type* data(void)
    {
        return m_vector;
    }

    /// \returns True if the vector is empty.
    ///
    bool empty(void) const
    {
        return m_vector_elems == 0;
    }

    /// Remove the specified element
    /// \param p_index The index of the lement to remove.
    ///
    void remove(size_t p_index)
    {
        assert(p_index < m_vector_elems);
        for (size_t i = p_index; i < m_vector_elems-1; ++i)
        {
            m_vector[i] = m_vector[i+1];
        }
        --m_vector_elems;
    }

    /// Removes the last element in the vector.
    ///
    void pop_back(void)
    {
        if (m_vector_elems)
        {
            --m_vector_elems;
        }
    }

    /// Removes the first element in the vector.
    ///
    void pop_front(void)
    {
        if (m_vector_elems)
        {
            remove(0);
        }
    }

    /// Adds a new element at the end of the vector, after its current last element.
    /// \param p_value Reference to the value to add.
    /// \returns False on error, such as out of memory.
    ///
    bool push_back(const Type& p_value)
    {
        if (!reserve(size() + 1))
        {
            return false;
        }
        m_vector[m_vector_elems++] = p_value;
    }

    /// Adds a new element at the front of the vecotr, which becomes the first element.
    /// \param p_value Reference to the value to add.
    ///
    bool push_front(const Type& p_value)
    {
        if (!reserve(size() + 1))
        {
            return false;
        }
        for (size_t i = 0; i < m_vector_elems; ++i)
        {
            m_vector[i+1] = m_vector[i];
        }
        m_vector[0] = p_value;
        ++m_vector_elems;
        return true;
    }

    /// Requests that the vector capacity be at least enough to contain p_size elements.
    /// \param p_size The minimum capacity requested.
    ///
    static const size_t m_grow_quantum = 16;
    bool reserve(size_t p_size)
    {
        if (p_size < m_vector_max)
        {
            return true;
        }
        size_t new_size = m_vector_max + m_grow_quantum;
        Type* new_vector = new Type[new_size];
        if (!new_vector)
        {
            return false;
        }
        for (size_t i = 0; i < m_vector_elems; ++i)
        {
            new_vector[i] = m_vector[i];
        }
        delete [] m_vector;
        m_vector = new_vector;
        m_vector_max = new_size;
        return true;
    }

    /// \returns The number of elements in the vector.
    ///
    size_t size(void) const
    {
        return m_vector_elems;
    }

  protected:
    Type*       m_vector;           // Pointer to a vector of Type objects
    size_t      m_vector_elems;     // Number of valid elements in m_vector
    size_t      m_vector_max;       // Maximum number of elements in m_vector
};

#endif // __Array_h_


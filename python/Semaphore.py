#
# Class for modeling a Semaphore in SigOS
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

import sys
import machine
from machine import Pin, PWM


class Semaphore:

    # Create a Semaphore object
    # @param p_head_id The identifier (number) of the Head containing this semaphore,
    #        1 is the highest head, 2 is the next highest, etc.
    #        Please note that a Head may have only zero or one semaphores.
    # @param p_gpio_pin The GPIO pin number driving the server signal
    # @param p_degrees_per_second Speed in which the Semaphore flag moves
    # @param p_0_degrees_pwd Servo PWM value for 0 degrees
    # @param p_90_degrees_pwm Servo PWM value for 90 degrees
    #
    def __init__(self, p_head_id, p_gpio_pin, p_degrees_per_second, p_0_degrees_pwm, p_90_degrees_pwm):
        self.m_head_id = p_head_id
        self.m_gpio_pin = p_gpio_pin
        self.m_degrees_per_second = p_degrees_per_second
        self.m_degrees_0_pwm = p_0_degrees_pwm
        self.m_degrees_90_pwm = p_90_degrees_pwm

    # Destructor - shut down PWM
    #
    def __del__(self):
        if self.m_servo:
            self.m_servo.deinit()


    # Initialize the servo hardware, must be called prior to set_servo_angle()
    #
    def init_hardware(self):
        # Setup PWM hardware for server signal
        self.m_servo_pwm_freq = 50 # freq=50 is required for servos
        self.m_servo_pwm_duty = 40 # servo flag low-position
        self.m_servo = PWM(Pin(self.m_gpio_pin), freq=self.m_servo_pwm_freq, duty=self.m_servo_pwm_duty)
        self.set_aspect(90)


    # Set a new aspect for the semaphore flag
    # @p_angle The angle of the flag, 0, 45, or 90
    # @returns True on succes, False on state mismatch
    #
    def set_aspect(self, p_angle):
        # Convert from angle to percent
        ratio = 100 / 90
        percent = p_angle * ratio
        # Convert percent to duty
        min = self.m_degrees_0_pwm
        max = self.m_degrees_90_pwm
        delta = max - min
        if min > max:
            # Swap min and max and invert percent
            temp = min
            min = max
            max = temp
            delta = max - min
            percent = 100 - percent
        duty = (delta * percent) / 100
        duty += min
        self.set_servo_duty(duty)
        # TODO: Add support for degrees-per-second


    # Set the angular position of the semaphore flag
    # @param p_duty The duty cycle value of the servo waveform
    #
    def set_servo_duty(self, p_duty):
        p_duty = int(p_duty)
        self.m_servo_pwm_duty = p_duty
        self.m_servo.duty(p_duty)


    # @returns A string representation of this Semaphore
    #
    def __str__(self):
        s = "  semaphore: "
        s += "\n    head-id: "
        s += str(self.m_head_id)
        s += "\n    degrees-per-second: "
        s += str(self.m_degrees_per_second)
        return s


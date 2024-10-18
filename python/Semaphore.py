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
from machine import Pin, PWM, Timer
import Light


class Semaphore:

    # Class variable for holding instances of Semaphore
    c_semaphore_list = list()

    # Class variable for generating timer id's
    c_timer_id = 0

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
        pwm_per_90degrees = abs(p_90_degrees_pwm - p_0_degrees_pwm)
        pwm_per_degree = pwm_per_90degrees / 90.0
        self.m_pwm_per_second = pwm_per_degree * p_degrees_per_second
        self.m_pwm_duty = None
        self.m_pwm_step = None
        self.m_pwm_target = None
        self.m_servo_moving = False
        self.m_angle_target = None
        self.m_servo = None
        self.m_timer = None

        # Keep a local list of Semaphores
        Semaphore.c_semaphore_list.append(self)

    # Destructor
    #
    def __del__(self):
        if self.m_servo:
            self.m_servo.deinit()
        if self.m_timer:
            self.m_timer.deinit()


    # Initialize the servo hardware, must be called prior to set_servo_angle()
    #
    @classmethod
    def InitHardware(p_class, p_config):
        for semaphore in p_class.c_semaphore_list:
            semaphore.init_hardware()


    # Modify the aspect of the specified semaphore
    # @param p_head_id Specifies the head containing the semaphore
    # @param p_angle The new angle for the semaphore flag
    # @param p_log Log to write failure messages to
    # @returns True on success, False on error
    #
    @classmethod
    def ChangeSemaphoreAspect(p_class, p_head_id, p_angle, p_log):
        for semaphore in p_class.c_semaphore_list:
            if p_head_id == semaphore.m_head_id:
                # change the aspect
                return semaphore.set_aspect(p_angle)
        p_log.add("Hardware", "No matching Semaphore 202410160900")
        return False


    # @returns The number of created Semaphore objects
    #
    @classmethod
    def Count(p_class):
        return len(p_class.c_semaphore_list)


    # Adjust servos that are in the process of changing state
    #
    @classmethod
    def AdjustDuty(p_class):
        for semaphore in p_class.c_semaphore_list:
            semaphore.adjust_duty()


    # Initialize the servo hardware, must be called prior to set_servo_angle()
    #
    def init_hardware(self):
        # Setup PWM hardware for server signal
        pwm_freq = 50 # freq=50 is required for servos
        self.m_pwm_duty = self.m_degrees_90_pwm # servo flag low-position
        self.m_pwm_target = self.m_degrees_90_pwm
        self.m_angle_target = 90
        self.m_servo = PWM(Pin(self.m_gpio_pin), freq=pwm_freq, duty=self.m_pwm_duty)

        # Create and start timer
        self.m_timer = machine.Timer(Semaphore.c_timer_id)
        pwm_per_second = int(self.m_pwm_per_second)
        self.m_timer.init(mode=Timer.PERIODIC, freq=pwm_per_second, callback=servo_callback)


    # Convert from degrees to PWM duty cycle
    # @p_angle The angle of the flag, 0, 45, or 90
    # @returns PWM duty cycle
    #
    def degrees_to_pwm(self, p_angle):
        # Convert from angle to percent
        ratio = 100.0 / 90.0
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
            percent = 100. - percent
        duty_offset = (delta * percent) / 100.0
        duty = min + duty_offset
        return duty


    # Adjust the duty cycle by 1 and restart timer if necessary
    #
    def adjust_duty(self):
        if not self.m_servo_moving:
            return

        # Compute the new duty from the old self.m_pwm_duty
        new_duty = self.m_pwm_duty
        if int(new_duty) < int(self.m_pwm_target):
            new_duty += 1
        elif int(new_duty) > int(self.m_pwm_target):
            new_duty -= 1
        else:
            # Re-enable light output
            Light.Light.Inhibit(self.m_head_id, False)
            # Movement complete
            self.m_servo_moving = False

        # Update the servo position
        self.set_servo_duty(new_duty)


    # Set a new aspect for the semaphore flag
    # @p_angle The angle of the flag, 0, 45, or 90
    # @returns True on succes, False on state mismatch
    #
    def set_aspect(self, p_angle):
        # Update targets to new request
        self.m_angle_target = p_angle
        duty = self.degrees_to_pwm(p_angle)
        self.m_pwm_target = duty
        if int(self.m_pwm_target) != int(self.m_pwm_duty):
            self.m_servo_moving = True
            # Inhibit light output during movement
            Light.Light.Inhibit(self.m_head_id, True)
        return True


    # Set the angular position of the semaphore flag
    # @param p_duty The duty cycle value of the servo waveform
    #
    def set_servo_duty(self, p_duty):
        duty = int(p_duty)
        self.m_pwm_duty = duty
        self.m_servo.duty(duty)


    # @returns A string representation of this Semaphore
    #
    def __str__(self):
        s = "  semaphore: "
        s += "\n    head-id: "
        s += str(self.m_head_id)
        s += "\n    degrees-per-second: "
        s += str(self.m_degrees_per_second)
        return s


# Timer callback to adjust the servo duty cycle
#
def servo_callback(p_timer):
    Semaphore.AdjustDuty()



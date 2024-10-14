#
# Defines Hardware interfaces for SigOS
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

# Nomenclature: B, B-, B+
# B means the block protected by the semaphore
# B- means the block immediately preceeding the protected block B
# B+ means the block immediately following the protected block B
# This nomenclature is in respect to the direction of the train
# moving from B- into B and viewing the semaphore's face

import sys
import machine
import ubinascii

class Hardware:

    # Determine underlying hardware and initialize pins
    #
    def __init__(self):
        self.m_platform = sys.platform
        self.m_unique_id = ubinascii.hexlify(machine.unique_id())

        self.m_led_pwm_freq = 1000
        self.m_led_pwm_duty_u16 = 65535/2
        if (self.m_platform == 'esp8266'):
            # ESP8266 pinout
            # Pin 1 - GND
            # Pin 2 - On-board LED and PWM for semaphore light/LED
            # Pin 3 - Detect B
            # Pin 4 - Detect B-
            # Pin 5 - Servo control out - GND at power-on to program
            # Pin 6 - /Reset (unused)
            # Pin 7 - Detect B+
            # Pin 8 - VCC
            self.m_led = PWM(Pin(2), freq=self.m_led_pwm_freq, duty_u16=self.m_led_pwm_duty_u16)

            self.m_servo_pwm_freq = 50 # freq=50 is required for servos
            self.m_servo_pwm_duty = 40 # servo flag low-position
            self.m_servo = PWM(Pin(5), freq=self.m_servo_pwm_freq, duty=self.m_servo_pwm_duty)

            self.m_detect_b  = Pin(3, Pin.IN, Pin.PULL_UP)
            self.m_detect_bm = Pin(4, Pin.IN, Pin.PULL_UP)
            self.m_detect_bp = Pin(7, Pin.IN, Pin.PULL_UP)
        elsif (self.m_platform == 'esp32'):
            # ESP32 S2 mini pins used - tries to use same "pin" numbers as ESP8266
            # Pin 2 - LED light
            # Pin 3 - detect block B
            # Pin 4 - detect block B-
            # Pin 5 - Servo control out
            # Pin 7 - detect block B+
            self.m_led = PWM(Pin(2), freq=self.m_led_pwm_freq, duty_u16=self.m_led_pwm_duty_u16)

            self.m_servo_pwm_freq = 50 # freq=50 is required for servos
            self.m_servo_pwm_duty = 40 # servo flag low-position
            self.m_servo = PWM(Pin(5), freq=self.m_servo_pwm_freq, duty=self.m_servo_pwm_duty)

            self.m_detect_b  = Pin(3, Pin.IN, Pin.PULL_UP)
            self.m_detect_bm = Pin(4, Pin.IN, Pin.PULL_UP)
            self.m_detect_bp = Pin(7, Pin.IN, Pin.PULL_UP)
        else:
            raise Exception('Unrecognized hardware {} 02407241136', self.m_platform)

    # Destructor - shut down PWM
    #
    def __del__(self):
        self.m_led.deinit()
        self.m_servo.deinit()


    # Set the Lumen intensity level of the LED
    # @param p_percent A percent value between 0 (off) and 100 (max intensity)
    #
    def set_led_light(self, p_percent)
        duty = 65535 * p_percent
        if (duty > 0):
            duty /= 100
        self.m_led_pwm_duty_u16 = duty
        self.m_led.duty_u16(duty)


    # Set the angular position of the semaphore flag
    # @param p_percent A percent value between 0 (fully down) and 100 (fully up)
    #
    def set_servo_angle(self, p_percent)
        min = 40
        max = 115
        duty = (max - min) * p_percent
        if (duty > 0):
            duty /= 100
        duty += min
        self.m_servo_pwm_duty = duty
        self.m_servo.duty(duty)


    def neopixel(self):
        # Set GPIO0 to output to drive NeoPixels
        pin = Pin(0, Pin.OUT)

        # create NeoPixel dirver on GPIO0 for 8 pixels
        np = NeoPixel(pin, 8)

        # Set the first pixel to while
        np[0] = (255, 255, 255)

        # Write data to all pixels
        np.write()

        # Get first pixel color
        r, g, b = np[0]


    # @returns True if the B input signal has detected a train
    #
    def get_detect_b(self)
        return self.m_detect_b.value()


    # @returns True if the B- input signal has detected a train
    #
    def get_detect_bm(self)
        return self.m_detect_bm.value()


    # @returns True if the B+ input signal has detected a train
    #
    def get_detect_bp(self)
        return self.m_detect_bp.value()


# Date: Dec 12, 2020
# Author: Code orginally from SunFounder Steam Education
# Sunfounder - Da Vinci Kit for Raspberry Pi
# Modified by Andrew Palmer, OTHS Technology Teacher
# Program Name: 2 Servo Controlled by Thumb Joystick.py
# This program controls two servo motors based on the feedback from a thumb joystick
# The code works, but the motors twitch alot.  So when I get a chance I will upgrade the code.

#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import ADC0834

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
ServoPin1 = 24
ServoPin2 = 25


def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin


def setup():
    global p
    global p2
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by BCM
    GPIO.setup(ServoPin1, GPIO.OUT)  # Set ServoPin's mode is output
    GPIO.output(ServoPin1, GPIO.LOW)  # Set ServoPin to low
    p = GPIO.PWM(ServoPin1, 50)  # set Frequecy to 50Hz
    p.start(0)  # Duty Cycle = 0
    GPIO.setup(ServoPin2, GPIO.OUT)  # Set ServoPin's mode is output
    GPIO.output(ServoPin2, GPIO.LOW)  # Set ServoPin to low
    p2 = GPIO.PWM(ServoPin2, 50)  # Set ServoPin to low
    p2.start(0)
    ADC0834.setup()  # added from the Joystick program


def setAngleX(angle):  # make the servo rotate to specific angle (0-180 degrees)
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)  # map the angle to duty cycle and output it


def setAngleY(angle):  # make the servo rotate to specific angle (0-180 degrees)
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p2.ChangeDutyCycle(pwm)  # map the angle to duty cycle and output it


def loop():
    while True:
        x_val = ADC0834.getResult(0)  # added from the Joystick program
        y_val = ADC0834.getResult(1)  # added from the Joystick program
        setAngleX(x_val)
        time.sleep(0.75)
        setAngleY(y_val)
        time.sleep(0.75)


def destroy():
    p.stop()
    p2.stop()
    GPIO.cleanup()


if __name__ == "__main__":  # Program start from here
    setup()
    try:
        loop()
    except (
        KeyboardInterrupt
    ):  # When 'Ctrl+C' is pressed, the program destroy() will be executed.
        destroy()

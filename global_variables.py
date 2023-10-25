"""
Name: Jinyuan Zhao
Date: 2023-10-24
Program Title: global_variables.py
Description: This is a file that stores global variables and functions.
"""

import RPi.GPIO as GPIO
import Adafruit_DHT
import ADC0834

# configure GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# configure the servo
SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500

servo_pin_1 = 19
servo_pin_2 = 20

# global variables (unused)
curr_x_val = 0
curr_y_val = 0
is_monitoring = False

"""
This function gets the temperature and humidity from the DHT11 sensor.
"""
def get_temperature_and_humidity():

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    return temperature, humidity

"""
This function maps a value from one range to another.
"""
def map(value, in_min, in_max, out_min, out_max):

    return (out_max - out_min) * (value - in_min) / (in_max - in_min) + out_min

"""
This function is called when the window is closed.
"""
def setup():

    # global variables
    global p
    global p2

    # configure the servo
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin_1, GPIO.OUT)
    GPIO.output(servo_pin_1, GPIO.LOW)

    p = GPIO.PWM(servo_pin_1, 50)
    p.start(0)

    GPIO.setup(servo_pin_2, GPIO.OUT)
    GPIO.output(servo_pin_2, GPIO.LOW)

    p2 = GPIO.PWM(servo_pin_2, 50)
    p2.start(0)

    # configure the ADC
    ADC0834.setup()

"""
Sets the x angle of the servo.
"""
def set_angle_x(angle):

    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)

"""
Sets the y angle of the servo.
"""
def set_angle_y(angle):

    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p2.ChangeDutyCycle(pwm)

"""
This function is called when the window is closed.
"""
def destroy():

    p.stop()
    p2.stop()

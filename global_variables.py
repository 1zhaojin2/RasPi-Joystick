from colorsys import rgb_to_hls
import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import cooldown, BucketType
import time
import lirc
import RPi_I2C_driver
import RPi.GPIO as GPIO
import Adafruit_DHT
import openai
import ADC0834


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500
ServoPin1 = 19
ServoPin2 = 20

curr_x_val = 0
curr_y_val = 0


def get_temperature_and_humidity():

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    return temperature, humidity



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
        setAngleY(y_val)


def destroy():
    p.stop()
    p2.stop()
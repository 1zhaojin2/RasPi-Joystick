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

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500 

ServoPin1 = 19
ServoPin2 = 20

def map(value, inMin, inMax, outMin, outMax):
    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
ADC0834.setup()
global p
global p2
GPIO.setup(ServoPin1, GPIO.OUT)
GPIO.setup(ServoPin2, GPIO.OUT)
GPIO.output(ServoPin1, GPIO.LOW)
GPIO.output(ServoPin2, GPIO.LOW)
p = GPIO.PWM(ServoPin1, 50)
p2 = GPIO.PWM(ServoPin2, 50)
p.start(0)
p2.start(0)

joystick_x_value = 0
joystick_y_value = 0

def setAngle1(angle):
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)

def setAngle2(angle):  
    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p2.ChangeDutyCycle(pwm)

def get_temperature_and_humidity():

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    return temperature, humidity

def moveServo1(angle):
    p.ChangeDutyCycle(2.5 + 10 * angle / 180)
    time.sleep(0.02)
    p.ChangeDutyCycle(0)   

def moveServo2(angle):
    p2.ChangeDutyCycle(2.5 + 10 * angle / 180)
    time.sleep(0.02)
    p2.ChangeDutyCycle(0)

def destroy():
    p.stop()
    p2.stop()
    GPIO.cleanup()

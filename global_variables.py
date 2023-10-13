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
ADC0834.setup()


def get_temperature_and_humidity():

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    return temperature, humidity


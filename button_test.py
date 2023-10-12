import RPi.GPIO as GPIO
import RPi_I2C_driver
from time import *
import time

mylcd = RPi_I2C_driver.lcd()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

currText = "Button Released"


while True:
    input_state = GPIO.input(16)
    if input_state == False:
        if(currText != "Button Pressed"):
            currText = "Button Pressed"

            mylcd.lcd_clear()
            mylcd.lcd_display_string("Button Pressed", 1)


        
    else:

        if(currText != "Button Released"):
            currText = "Button Released"

            mylcd.lcd_clear()
            mylcd.lcd_display_string("Button Released", 1)

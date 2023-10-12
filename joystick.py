import RPi.GPIO as GPIO
import ADC0834
import time

BtnPin = 22

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    ADC0834.setup()

def destroy():
    GPIO.cleanup()

def loop():
    while True:
        x_val = ADC0834.getResult(0)
        y_val = ADC0834.getResult(1)
        Btn_val = GPIO.input(BtnPin)
        print('X: %d Y:%d Btn:%d' % (x_val, y_val, Btn_val))
        time.sleep(0.2)


if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
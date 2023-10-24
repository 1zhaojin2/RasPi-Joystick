import RPi.GPIO as GPIO
import Adafruit_DHT
import ADC0834


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500

servo_pin_1 = 19
servo_pin_2 = 20

curr_x_val = 0
curr_y_val = 0

is_monitoring = False


def get_temperature_and_humidity():

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    return temperature, humidity

def map(value, in_min, in_max, out_min, out_max):

    return (out_max - out_min) * (value - in_min) / (in_max - in_min) + out_min

def setup():

    global p
    global p2

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

    ADC0834.setup()

def set_angle_x(angle):

    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)

def set_angle_y(angle):

    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p2.ChangeDutyCycle(pwm)

def destroy():

    p.stop()
    p2.stop()
    is_monitoring = False

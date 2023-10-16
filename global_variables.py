import RPi.GPIO as GPIO
import Adafruit_DHT
import ADC0834


GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

SERVO_MIN_PULSE = 500
SERVO_MAX_PULSE = 2500

ServoPin1 = 19
ServoPin2 = 20

curr_x_val = 0
curr_y_val = 0

isMonitoring = False


def get_temperature_and_humidity():

    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    return temperature, humidity

def map(value, inMin, inMax, outMin, outMax):

    return (outMax - outMin) * (value - inMin) / (inMax - inMin) + outMin

def setup():

    global p
    global p2

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ServoPin1, GPIO.OUT)
    GPIO.output(ServoPin1, GPIO.LOW)

    p = GPIO.PWM(ServoPin1, 50)
    p.start(0)

    GPIO.setup(ServoPin2, GPIO.OUT)
    GPIO.output(ServoPin2, GPIO.LOW)

    p2 = GPIO.PWM(ServoPin2, 50)
    p2.start(0)

    ADC0834.setup()

def setAngleX(angle):

    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p.ChangeDutyCycle(pwm)

def setAngleY(angle):

    angle = max(0, min(180, angle))
    pulse_width = map(angle, 0, 180, SERVO_MIN_PULSE, SERVO_MAX_PULSE)
    pwm = map(pulse_width, 0, 20000, 0, 100)
    p2.ChangeDutyCycle(pwm)

def loop():

    while True:
        x_val = ADC0834.getResult(0)
        y_val = ADC0834.getResult(1)

        setAngleX(x_val)
        setAngleY(y_val)

def destroy():

    p.stop()
    p2.stop()
    isMonitoring = False

def get_joystick_values():
    
    return curr_x_val, curr_y_val
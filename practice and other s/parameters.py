import time
import board
import pwmio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import servo
from sonarbit import Sonarbit

pwm1 = pwmio.PWMOut(board.D0, frequency=50)
pwm2 = pwmio.PWMOut(board.D1, frequency=50)

m1 = servo.ContinuousServo(pwm1)
m2 = servo.ContinuousServo(pwm2)

def stop():
    m1.throttle = 0.0
    m2.throttle = 0.0

def move_forward():
    m1.throttle = -0.5
    m2.throttle = 0.5
    time.sleep(1)
    stop()


def move_right90():
    m1.throttle = -0.5
    m2.throttle = -0.5
    time.sleep(0.8)
    stop()

def turn180():
    m1.throttle = -0.5
    m2.throttle = -0.5
    time.sleep(1.7)
    stop()

def square():
    for i in range(1, 5):
        move_forward()
        move_right90()

def random_shape1(): #hexagon
    for i in range(1, 7):
        move_forward()
        move_right90()
        turn180()

random_shape1()


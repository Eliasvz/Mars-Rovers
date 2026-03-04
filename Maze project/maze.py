import time
import board
import pwmio
from adafruit_motor import servo
from sonarbit import Sonarbit


pwm1 = pwmio.PWMOut(board.D0, frequency=50)
pwm2 = pwmio.PWMOut(board.D1, frequency=50)

m1 = servo.ContinuousServo(pwm1)
m2 = servo.ContinuousServo(pwm2)


distance_sensor_F = Sonarbit(board.D7)
distance_sensor_R = Sonarbit(board.D5)
prev_distance = 570

state = check_sensors#nothing yet

def check_sensors():
    distance_R = distance_sensor_R.get_distance(prev_distance)
    print("The object is: " + str(distance_R) + " cm away")


def move_forward():
    m1.throttle = -0.5
    m2.throttle = 0.5
    time.sleep(2)  # still have to figure out appropiate time for 30cm
    stop()
    time.sleep(1)

def move_right():
    m1.throttle = -0.5
    m2.throttle = -0.5
    time.sleep(0.8)
    stop()
    time.sleep(1)


def turn180():
    m1.throttle = -0.5
    m2.throttle = -0.5
    time.sleep(1.6)
    stop()
    time.sleep(1)


def stop():
    m1.throttle = 0.0
    m2.throttle = 0.0

while True:
    move_right()

if state == check_sensors:
    check_sensors()
elif state == move_forward:
    move_forward()
elif state == move_right:
    move_right()
elif state == turn180:
    turn180()




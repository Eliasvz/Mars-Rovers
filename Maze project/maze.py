import time
import board
import pwmio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import servo
from sonarbit import Sonarbit

# init led

Led_right = DigitalInOut(board.D3)
Led_right.direction = Direction.OUTPUT

Led_forward = DigitalInOut(board.D4)
Led_forward.direction = Direction.OUTPUT

pwm1 = pwmio.PWMOut(board.D0, frequency=50)
pwm2 = pwmio.PWMOut(board.D1, frequency=50)

m1 = servo.ContinuousServo(pwm1)
m2 = servo.ContinuousServo(pwm2)

distance_sensor_F = Sonarbit(board.D7)
distance_sensor_R = Sonarbit(board.D5)

prev_distance_F = 570
prev_distance_R = 570


state = "check_sensors"


def check_sensors():
    global state
    distance_R = distance_sensor_R.get_distance(prev_distance_R)
    print("The object is: " + str(distance_R) + " cm away to the right")
    time.sleep(0.5)
    if distance_R <= 15:
        distance_F = distance_sensor_F.get_distance(prev_distance_F)
        print("The object is: " + str(distance_F) + " cm away from the front")
        time.sleep(0.5)
        if distance_F <= 15:
            state = "turn180"
        else:
            state = "move_forward"
    else:
        state = "move_right"


def move_forward():
    global state
    m1.throttle = -0.5
    m2.throttle = 0.6
    time.sleep(2)
    stop()
    time.sleep(1)
    state = "check_sensors"


def move_right():
    global state
    m1.throttle = -0.5
    m2.throttle = -0.5
    time.sleep(1.7)
    stop()
    time.sleep(1)
    move_forward()
    stop()
    time.sleep(1)
    state = "check_sensors"


def turn180():
    global state
    m1.throttle = -0.5
    m2.throttle = -0.5
    time.sleep(3.3)
    stop()
    time.sleep(1)
    state = "check_sensors"


def stop():
    m1.throttle = 0.0
    m2.throttle = 0.0


while True:
    print("current state is: " + state)

    if state == "check_sensors":
        check_sensors()

    elif state == "move_forward":
        Led_right.value = True
        Led_forward.value = False
        move_forward()

    elif state == "move_right":
        Led_right.value = False
        Led_forward.value = False
        move_right()

    elif state == "turn180":
        Led_right.value = True
        Led_forward.value = True
        turn180()

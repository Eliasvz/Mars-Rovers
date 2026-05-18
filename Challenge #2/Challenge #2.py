import board
from rc import RCReceiver
import time
import pwmio
from adafruit_motor import servo
from adafruit_simplemath import map_range
from i2cdisplaybus import I2CDisplayBus
import adafruit_displayio_ssd1306
import displayio
from elapsed_time import ElapsedTime
import busio
import adafruit_apds9960.apds9960
import terminalio

rc = RCReceiver(ch1=board.D10, ch2=board.D11, ch5=board.D12, ch6=board.D13)

displayio.release_displays()

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)
sensor.enable_color = True

total_r = 0
total_g = 0
total_b = 0

avg_r = 0
avg_g = 0
avg_b = 0

amount_of_reads = 0

display_bus = I2CDisplayBus(i2c, device_address=0x3d)  # or 0x3d
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)


left_pwm = pwmio.PWMOut(board.D0, frequency=50)
right_pwm = pwmio.PWMOut(board.D1, frequency=50)
drive_left = servo.ContinuousServo(left_pwm)
drive_right = servo.ContinuousServo(right_pwm)

turn_left_pwm = pwmio.PWMOut(board.D2, frequency=50)
turn_right_pwm = pwmio.PWMOut(board.D3, frequency=50)
turn_left = servo.Servo(turn_left_pwm)
turn_right = servo.Servo(turn_right_pwm)

angle = 90

drill_pwm = pwmio.PWMOut(board.D5, frequency=50)
drill_drilling = servo.ContinuousServo(drill_pwm)

drive_state = "STOP"

drill_state = "OFF"  # needs off, down, up, finished

drill_down_timer = ElapsedTime()
drill_up_timer = ElapsedTime()

read_increment_timer = ElapsedTime()


def update_drive_state(drive_state, joystick, throttle):
    global angle
    print(drive_state)
    if drive_state == "DRIVE":

        joystick_range = map_range(joystick, -1, 1, 0, 100)

        if joystick_range > 55:
            angle += 1
            if angle > 180:
                angle = 180

        elif joystick_range < 45:
            angle -= 1
            if angle < 0:
                angle = 0

        if throttle == 0:
            drive_left.throttle = 0
            drive_right.throttle = 0

        else:
            drive_left.throttle = throttle
            drive_right.throttle = throttle

        turn_left.angle = angle
        turn_right.angle = angle

    print("speed", throttle, "angle", angle)

   if drive_state == "STOP":
        drive_left.throttle = 0
        drive_right.throttle = 0


def update_drill_state(drill_switch):
    global drill_state
    print(drill_state)

    if drill_switch == 0:
        drill_state = "OFF"
        drill_drilling.throttle = 0

    elif drill_switch == 1 and drill_state == "OFF":
        drill_state = "DOWN"
        drill_down_timer.reset()

    elif drill_state == "DOWN":

        if drill_down_timer.seconds() < 2:
            drill_drilling.throttle = 0.1
            print("DRILLING")
        else:
            drill_drilling.throttle = 0
            if amount_of_reads < 3:
                print("READING")
                if read_increment_timer.seconds() > 0.33:
                    r, g, b = sensor.color_data

                    total_r =+ r
                    total_g =+ g
                    total_b =+ b

                    amount_of_reads =+ 1
                    read_increment_timer.reset()
            else:
                avg_r = total_r/3
                avg_g = total_g/3
                avg_b = total_b/3

                print("Average", avg_r, avg_g, avg_b)

                drill_up_timer.reset()
                drill_state = "UP"

    elif drill_state == "UP":
        if drill_up_timer.seconds()< 2:
            drill_drilling.throttle = -0.1
        else:
            drill_drilling.throttle = 0
            drill_state = "FINISHED"

    elif drill_state == "FINISHED":
        drill_drilling.throttle = 0


drill_down_timer.reset()
drill_up_timer.reset()

read_increment_timer.reset()

while True:
    joystick = rc.read_channel(1)
    throttle = rc.read_channel(2)
    drill_switch = rc.read_channel(5)
    switch = rc.read_channel(6)

    if drill_switch == 1:
        drive_state = "STOP"
    if switch == 0:
        drive_state = "STOP"
    elif switch == 1 and drill_switch == 0:
        drive_state = "DRIVE"
    update_drive_state(drive_state, joystick, throttle)
    update_drill_state(drill_switch)
    time.sleep(0.02)

import board
from rc import RCReceiver
from arcade_drive import Drive
import time
import pwmio
from adafruit_motor import servo

# Initialize the receiver with designated pins for channels
rc = RCReceiver(ch1=board.D0, ch2=board.D1, ch5=board.D2, ch6=board.D3)
robot = Drive(motor_type="servo", left_pin=board.D4, right_pin=board.D5, scale = 1.0)

# Main code loop
while True:
    spin = rc.read_channel(1)
    throttle = rc.read_channel(2)
    ch5 = rc.read_channel(5)
    ch6 = rc.read_channel(6)

    # Print the channel values to the console
    print("Ch 1:", spin, "Ch 2:", throttle, "Ch 5:", ch5, "Ch 6:", ch6)
    robot.drive(spin, throttle)

    time.sleep(0.02) # add a minor sleep to keep in time with PWM cycle
# Write your code here :-)
